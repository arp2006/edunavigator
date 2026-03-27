from sqlalchemy.orm import Session
from app.models import UserProfile, SubjectResponse, Score


def combine_score(interest, performance):
    return (interest * 0.6) + (performance * 0.4)


def process_questionnaire(user_id, data, db: Session):
    # 1. get profile
    profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()

    if not profile:
        return None

    # 2. clear old responses (optional but recommended)
    db.query(SubjectResponse).filter(SubjectResponse.profile_id == profile.id).delete()

    # 3. store new responses
    for item in data.responses:
        response = SubjectResponse(
            profile_id=profile.id,
            subject=item.subject,
            interest=item.interest,
            performance=item.performance
        )
        db.add(response)

    # 4. get or create score
    score = db.query(Score).filter(Score.profile_id == profile.id).first()

    if not score:
        score = Score(profile_id=profile.id)
        db.add(score)

    # 5. reset scores
    score.math_score = 0
    score.science_score = 0
    score.commerce_score = 0
    score.tech_score = 0
    score.arts_score = 0

    # 6. calculate scores
    responses = db.query(SubjectResponse).filter(SubjectResponse.profile_id == profile.id).all()

    for res in responses:
        if res.interest is None or res.performance is None:
            continue

        combined = combine_score(res.interest, res.performance)

        if res.subject == "math":
            score.math_score += combined

        elif res.subject in ["physics", "chemistry", "biology"]:
            score.science_score += combined

        elif res.subject in ["accounts", "economics", "business"]:
            score.commerce_score += combined

    # 7. apply category boosts (NOW CORRECT)
    if data.extra:
        for category, answers in data.extra.items():
            category_score = sum(answers.values())
            boost = category_score * 0.25

            if category == "math":
                score.math_score += boost

            elif category == "science":
                score.science_score += boost

            elif category == "tech":
                score.tech_score += boost

            elif category == "commerce":
                score.commerce_score += boost

            elif category == "arts":
                score.arts_score += boost

    db.commit()

    return True