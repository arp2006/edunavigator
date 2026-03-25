from sqlalchemy.orm import Session
from app.models import Score, Degree


def generate_recommendations(profile_id, db: Session, top_n=5):
    # 1. get score
    score = db.query(Score).filter(Score.profile_id == profile_id).first()

    if not score:
        return []

    # 2. get degrees
    degrees = db.query(Degree).all()

    results = []

    for d in degrees:
        total = (
            score.math_score * d.math_weight +
            score.tech_score * d.tech_weight +
            score.arts_score * d.arts_weight +
            score.commerce_score * d.commerce_weight +
            score.science_score * d.science_weight
        )

        results.append({
            "degree_name": d.name,
            "type": d.type.name if d.type else "",
            "field": d.field.name if d.field else "",
            "discipline": d.discipline.name if d.discipline else "",
            "score": round(total, 2)
        })

    results.sort(key=lambda x: x["score"], reverse=True)

    return results[:top_n]