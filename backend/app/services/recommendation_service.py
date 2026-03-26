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
            (score.math_score or 0) * (d.math_weight or 0) +
            (score.tech_score or 0) * (d.tech_weight or 0) +
            (score.arts_score or 0) * (d.arts_weight or 0) +
            (score.commerce_score or 0) * (d.commerce_weight or 0) +
            (score.science_score or 0) * (d.science_weight or 0)
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