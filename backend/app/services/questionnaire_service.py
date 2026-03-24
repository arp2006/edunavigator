from app.models import UserProfile, Question, UserAnswer
from sqlalchemy.orm import Session
from app.services.recommendation_service import generate_recommendations

def process_and_store_answers(data, db: Session):
    user = db.query(UserProfile).filter(UserProfile.id == data.user_id).first()

    if not user:
        return None

    scores = {
        "math_score": 0,
        "tech_score": 0,
        "arts_score": 0,
        "commerce_score": 0,
        "science_score": 0
    }

    for item in data.answers:
        question = db.query(Question).filter(Question.id == item.question_id).first()

        if not question:
            continue

        # store answer
        user_answer = UserAnswer(
            user_id=data.user_id,
            question_id=item.question_id,
            answer=item.answer
        )
        db.add(user_answer)

        # scoring
        if item.answer == "yes":
            scores[f"{question.category}_score"] += question.weight

    # update profile
    user.math_score = scores["math_score"]
    user.tech_score = scores["tech_score"]
    user.arts_score = scores["arts_score"]
    user.commerce_score = scores["commerce_score"]
    user.science_score = scores["science_score"]

    db.commit()
    db.refresh(user)

    # 🔥 NEW — generate recommendations
    recommendations = generate_recommendations(user, db)

    return user, recommendations