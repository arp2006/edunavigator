import os
import json
import httpx
from sqlalchemy.orm import Session
from app.models import UserProfile, Score
from app.services.scoring_service import recompute_scores
from app.models import SubjectResponse

# ==============================
# CONFIG
# ==============================

LLM_MODE = os.getenv("LLM_MODE", "mock")  # "mock" or "real"

ANTHROPIC_API_URL = "https://api.anthropic.com/v1/messages"
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")

# ==============================
# MOCK PARSER (YOUR ORIGINAL LOGIC)
# ==============================

def detect_interests(msg: str):
    interest_keywords = {
        "coding": ["coding", "programming", "code", "software", "developer"],
        "design": ["design", "creative", "art", "draw", "visual"],
        "data": ["data", "analytics", "statistics", "numbers"],
        "health": ["health", "medicine", "biology", "doctor"],
        "business": ["business", "management", "finance", "marketing"],
        "research": ["research", "science", "experiment", "lab"],
        "teaching": ["teaching", "education", "students"],
        "machines": ["machines", "mechanical", "robot", "build"],
    }

    scores = {}

    for interest, keywords in interest_keywords.items():
        match_count = sum(1 for kw in keywords if kw in msg)
        if match_count > 0:
            scores[interest] = match_count

    return scores

# ✅ FIXED NEGATION (context aware)
def is_negative(msg: str, keywords: list):
    neg_words = ["not", "don't", "dont", "hate", "dislike"]

    for kw in keywords:
        for neg in neg_words:
            if f"{neg} {kw}" in msg or f"{kw} is not" in msg:
                return True
    return False

def convert_to_adjustments(msg: str):
    msg = msg.lower()

    interest_scores = detect_interests(msg)

    adj = {
        "math_score": 0,
        "science_score": 0,
        "tech_score": 0,
        "commerce_score": 0,
        "arts_score": 0
    }

    # ✅ COMPLETE mapping (fixed)
    mapping = {
        "coding": "tech_score",
        "data": "math_score",
        "health": "science_score",
        "business": "commerce_score",
        "design": "arts_score",
        "research": "science_score",
        "teaching": "arts_score",
        "machines": "tech_score",
    }

    for interest, strength in interest_scores.items():
        target = mapping.get(interest)

        if not target:
            continue

        # ✅ SMOOTH update (fixed)
        delta = min(strength * 0.5, 2)

        # ✅ NEGATION applied correctly
        if is_negative(msg, [interest]):
            adj[target] -= delta
        else:
            adj[target] += delta

    return adj, interest_scores


# ==============================
# MOCK CHAT (IMPROVED RESPONSE)
# ==============================

def mock_chat(message: str):
    adjustments, interest_scores = convert_to_adjustments(message)

    detected = list(interest_scores.keys())

    if detected:
        reply = f"Got it! I can see you're interested in {', '.join(detected)}."
    else:
        reply = "Thanks! Tell me a bit more about what you enjoy."

    return {
        "reply": reply,
        "adjustments": adjustments
    }


# ==============================
# REAL LLM (OPTIONAL)
# ==============================

def call_claude(profile: UserProfile, score: Score, history: list, user_message: str):
    system_prompt = """Return ONLY JSON:
{
  "reply": "...",
  "adjustments": {
    "math_score": 0,
    "science_score": 0,
    "tech_score": 0,
    "commerce_score": 0,
    "arts_score": 0
  }
}"""

    messages = [{"role": "user", "content": user_message}]

    response = httpx.post(
        ANTHROPIC_API_URL,
        headers={
            "x-api-key": ANTHROPIC_API_KEY,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        },
        json={
            "model": "claude-sonnet-4-20250514",
            "max_tokens": 300,
            "system": system_prompt,
            "messages": messages,
        },
        timeout=20,
    )

    response.raise_for_status()
    return json.loads(response.json()["content"][0]["text"])

# ==============================
# HELPERS
# ==============================

def clamp(val, min_v=1, max_v=5):
    return max(min(val, max_v), min_v)

# ==============================
# MAIN FUNCTION
# ==============================


def apply_adjustments_to_responses(profile_id: int, adjustments: dict, db: Session):

    responses = db.query(SubjectResponse).filter(
        SubjectResponse.profile_id == profile_id
    ).all()

    print("\n--- SCORE UPDATE START ---")
    print("ADJUSTMENTS:", adjustments)

    for r in responses:
        before = r.interest

        if r.subject == "math":
            r.interest = clamp(r.interest + adjustments.get("math_score", 0))
        elif r.subject == "science":
            r.interest = clamp(r.interest + adjustments.get("science_score", 0))
        elif r.subject == "tech":
            r.interest = clamp(r.interest + adjustments.get("tech_score", 0))
        elif r.subject == "commerce":
            r.interest = clamp(r.interest + adjustments.get("commerce_score", 0))
        elif r.subject == "arts":
            r.interest = clamp(r.interest + adjustments.get("arts_score", 0))
        
        after = r.interest

        print(f"{r.subject.upper()} → BEFORE: {before} | AFTER: {after}")

    print("--- SCORE UPDATE END ---\n")

    db.commit()

def process_chat(profile_id: int, message: str, db: Session) -> dict:
    profile = db.query(UserProfile).filter(UserProfile.id == profile_id).first()
    if not profile:
        return None

    history = list(profile.chat_history or [])

    try:
        if LLM_MODE == "mock":
            result = mock_chat(message)
        else:
            result = call_claude(profile, profile.score, history, message)
    except Exception:
        result = mock_chat(message)

    reply = result.get("reply", "Tell me more about your interests.")
    adjustments = result.get("adjustments", {})

    # ✅ DEBUG (keep during testing)
    print("ADJUSTMENTS:", adjustments)

    apply_adjustments_to_responses(profile.id, adjustments, db)

    # recompute scores
    recompute_scores(profile.id, db)

    # save history
    history.append({"role": "user", "content": message})
    history.append({"role": "assistant", "content": reply})
    profile.chat_history = history

    db.commit()
    db.refresh(profile)

    return {"reply": reply, "profile": profile}
