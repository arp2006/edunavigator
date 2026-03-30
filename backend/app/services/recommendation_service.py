from sqlalchemy.orm import Session
from app.models import Score, Degree, UserProfile


def is_degree_allowed(profile, degree):
    name = (degree.name or "").lower()

    if "btech" in name or "b.e" in name or "beng" in name:
        return profile.stream.lower() == "science"

    return True


def generate_recommendations(profile_id, db: Session, top_n=5):
    # 1. get profile + score
    profile = db.query(UserProfile).filter(UserProfile.id == profile_id).first()
    score = db.query(Score).filter(Score.profile_id == profile_id).first()

    if not profile or not score:
        return []

    # 2. get degrees
    degrees = db.query(Degree).all()

    results = []

    for d in degrees:

        # ------------------------------
        # STREAM CONSTRAINT
        # ------------------------------
        if not is_degree_allowed(profile, d):
            continue

        # ------------------------------
        # SCORE CALCULATION
        # ------------------------------
        math = score.math_score or 0
        tech = score.tech_score or 0
        arts = score.arts_score or 0
        commerce = score.commerce_score or 0
        science = score.science_score or 0

        total = (
            math * (d.math_weight or 0) +
            tech * (d.tech_weight or 0) +
            arts * (d.arts_weight or 0) +
            commerce * (d.commerce_weight or 0) +
            science * (d.science_weight or 0)
        )

        # ------------------------------
        # CONFIDENCE CALCULATION
        # ------------------------------
        max_possible = (
            5 * (d.math_weight or 0) +
            5 * (d.tech_weight or 0) +
            5 * (d.arts_weight or 0) +
            5 * (d.commerce_weight or 0) +
            5 * (d.science_weight or 0)
        )

        confidence = (total / max_possible * 100) if max_possible > 0 else 0

        # ------------------------------
        # EXPLANATION
        # ------------------------------
        reasons = []

        if math > 3 and (d.math_weight or 0) > 0:
            reasons.append("strong in math")

        if tech > 3 and (d.tech_weight or 0) > 0:
            reasons.append("interested in technology")

        if science > 3 and (d.science_weight or 0) > 0:
            reasons.append("good in science")

        if commerce > 3 and (d.commerce_weight or 0) > 0:
            reasons.append("inclined towards business")

        if arts > 3 and (d.arts_weight or 0) > 0:
            reasons.append("creative/artistic")

        explanation = ", ".join(reasons) if reasons else "general fit"

        # ------------------------------
        # RESULT
        # ------------------------------
        results.append({
            "degree_name": d.name,
            "type": d.type.name if d.type else "",
            "field": d.field.name if d.field else "",
            "discipline": d.discipline.name if d.discipline else "",
            "score": round(total, 2),
            "confidence": round(confidence, 1),
            "why": explanation
        })

    # ------------------------------
    # SORT + LIMIT
    # ------------------------------
    results.sort(key=lambda x: x["score"], reverse=True)

    return results[:top_n]