import os
import json
import httpx
from sqlalchemy.orm import Session
from app.models import UserProfile, Score

# ==============================
# CONFIG
# ==============================

LLM_MODE = os.getenv("LLM_MODE", "mock")  # "mock" or "real"

ANTHROPIC_API_URL = "https://api.anthropic.com/v1/messages"
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")

# ==============================
# MOCK PARSER (YOUR ORIGINAL LOGIC)
# ==============================

def parse_chat_input(message: str) -> dict:
    msg = message.lower()
    updates = {}
    reply_hints = []

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

    detected_interests = []
    for interest, keywords in interest_keywords.items():
        if any(kw in msg for kw in keywords):
            detected_interests.append(interest)

    if detected_interests:
        updates["interests"] = detected_interests
        reply_hints.append(f"interests in {', '.join(detected_interests)}")

    if any(w in msg for w in ["creative", "artistic", "design"]):
        updates["work_style"] = "creative"
        reply_hints.append("creative work style")
    elif any(w in msg for w in ["analytical", "logical", "math", "data"]):
        updates["work_style"] = "analytical"
        reply_hints.append("analytical work style")

    field_keywords = {
        "engineering": ["engineering", "tech", "computer"],
        "science": ["science", "biology", "physics"],
        "arts": ["arts", "psychology", "design"],
        "commerce": ["commerce", "business", "finance"],
    }

    preferred_fields = []
    for field, keywords in field_keywords.items():
        if any(kw in msg for kw in keywords):
            preferred_fields.append(field)

    if preferred_fields:
        updates["preferred_fields"] = preferred_fields
        reply_hints.append(f"preference for {', '.join(preferred_fields)}")

    if reply_hints:
        reply = f"Got it! Updated based on your {' and '.join(reply_hints)}."
    else:
        reply = "Thanks! I've noted your input."

    return {"updates": updates, "reply": reply}


def convert_updates_to_adjustments(updates: dict):
    adj = {
        "math_score": 0,
        "science_score": 0,
        "tech_score": 0,
        "commerce_score": 0,
        "arts_score": 0
    }

    interests = updates.get("interests", [])

    if "coding" in interests:
        adj["tech_score"] += 2
    if "data" in interests:
        adj["math_score"] += 1
    if "health" in interests:
        adj["science_score"] += 2
    if "business" in interests:
        adj["commerce_score"] += 2
    if "design" in interests:
        adj["arts_score"] += 2

    return adj


def mock_chat(message: str):
    parsed = parse_chat_input(message)
    return {
        "reply": parsed["reply"],
        "adjustments": convert_updates_to_adjustments(parsed["updates"])
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

def clamp(val):
    return max(min(val, 2), -2)

# ==============================
# MAIN FUNCTION
# ==============================

def process_chat(profile_id: int, message: str, db: Session) -> dict:
    profile = db.query(UserProfile).filter(UserProfile.id == profile_id).first()
    if not profile:
        return None

    score = profile.score
    history = list(profile.chat_history or [])

    # ------------------------------
    # SELECT MODE
    # ------------------------------
    try:
        if LLM_MODE == "mock":
            result = mock_chat(message)
        else:
            result = call_claude(profile, score, history, message)
    except Exception:
        # fallback to mock if LLM fails
        result = mock_chat(message)

    reply = result.get("reply", "Tell me more about your interests.")
    adjustments = result.get("adjustments", {})

    # ------------------------------
    # SAFE SCORE UPDATE
    # ------------------------------
    if score:
        score.math_score += clamp(adjustments.get("math_score", 0))
        score.science_score += clamp(adjustments.get("science_score", 0))
        score.tech_score += clamp(adjustments.get("tech_score", 0))
        score.commerce_score += clamp(adjustments.get("commerce_score", 0))
        score.arts_score += clamp(adjustments.get("arts_score", 0))

    # ------------------------------
    # SAVE CHAT HISTORY
    # ------------------------------
    history.append({"role": "user", "content": message})
    history.append({"role": "assistant", "content": reply})
    profile.chat_history = history

    db.commit()
    db.refresh(profile)

    return {"reply": reply, "profile": profile}