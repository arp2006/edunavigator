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

    for r in responses:
        category = r.subject  # or r.category depending on your model
        value = (r.interest + r.performance) / 2

        if category == "math":
            scores["math_score"] += value
        elif category == "science":
            scores["science_score"] += value
        elif category == "tech":
            scores["tech_score"] += value
        elif category == "commerce":
            scores["commerce_score"] += value
        elif category == "arts":
            scores["arts_score"] += value

    # update or create score row
    if not profile.score:
        profile.score = Score(**scores)
    else:
        for k, v in scores.items():
            setattr(profile.score, k, v)

    db.commit()