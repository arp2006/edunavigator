from sqlalchemy.orm import Session
from app.models import UserProfile, SubjectResponse, Score

def combine_score(interest, performance):
    return (interest * 0.6) + (performance * 0.4)


def calculate_scores(profile, responses):
    # reset
    profile.math_score = 0
    profile.science_score = 0
    profile.commerce_score = 0

    for res in responses:
        combined = combine_score(res.interest, res.performance)

        if res.subject == "math":
            profile.math_score += combined

        elif res.subject in ["physics", "chemistry", "biology"]:
            profile.science_score += combined

        elif res.subject in ["accounts", "economics", "business"]:
            profile.commerce_score += combined

def recompute_scores(profile_id: int, db: Session):
    profile = db.query(UserProfile).filter(UserProfile.id == profile_id).first()
    if not profile:
        return

    responses = db.query(SubjectResponse).filter(
        SubjectResponse.profile_id == profile_id
    ).all()

    scores = {
        "math_score": 0,
        "science_score": 0,
        "tech_score": 0,
        "commerce_score": 0,
        "arts_score": 0
    }

    category_map = {
        "math": "math_score",
        "physics": "science_score",
        "chemistry": "science_score",
        "biology": "science_score",
        "computer": "tech_score",
        "programming": "tech_score",
        "it": "tech_score",
        "accounts": "commerce_score",
        "business": "commerce_score",
        "history": "arts_score",
        "literature": "arts_score"
    }

    for r in responses:
        subject = r.subject.lower()
        value = (r.interest + r.performance) / 2

        target = category_map.get(subject)

        if target:
            scores[target] += value

    # debug (VERY useful)
    print("\n--- RECOMPUTED SCORES ---")
    for k, v in scores.items():
        print(f"{k.upper()}: {v}")

    if not profile.score:
        profile.score = Score(**scores)
    else:
        for k, v in scores.items():
            setattr(profile.score, k, v)

    db.commit()
    