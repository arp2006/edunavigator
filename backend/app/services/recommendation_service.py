from typing import List, Dict
from app.models import UserProfile, DegreeProgram


# ─── Degree Catalog ──────────────────────────────────────────────────────────
# In production this comes from the DB; here it's seeded as a fallback catalog.

DEGREE_CATALOG = [
    {
        "name": "Computer Science",
        "field": "engineering",
        "description": "Study of algorithms, programming, AI, and software systems.",
        "requires_math": 0.8, "requires_science": 0.6, "requires_arts": 0.2,
        "requires_commerce": 0.2, "requires_tech": 0.9,
        "tags": ["coding", "problem-solving", "AI", "software", "technology"]
    },
    {
        "name": "Mechanical Engineering",
        "field": "engineering",
        "description": "Design and analysis of physical systems and machinery.",
        "requires_math": 0.9, "requires_science": 0.8, "requires_arts": 0.2,
        "requires_commerce": 0.1, "requires_tech": 0.7,
        "tags": ["machines", "physics", "design", "manufacturing"]
    },
    {
        "name": "Business Administration",
        "field": "commerce",
        "description": "Management, finance, marketing, and organizational behavior.",
        "requires_math": 0.5, "requires_science": 0.2, "requires_arts": 0.5,
        "requires_commerce": 0.9, "requires_tech": 0.3,
        "tags": ["management", "finance", "leadership", "marketing", "business"]
    },
    {
        "name": "Psychology",
        "field": "arts",
        "description": "Study of human behavior, mental processes, and social dynamics.",
        "requires_math": 0.3, "requires_science": 0.5, "requires_arts": 0.8,
        "requires_commerce": 0.2, "requires_tech": 0.2,
        "tags": ["people", "behavior", "mental health", "counseling", "research"]
    },
    {
        "name": "Data Science",
        "field": "engineering",
        "description": "Statistics, machine learning, and data-driven decision making.",
        "requires_math": 0.9, "requires_science": 0.6, "requires_arts": 0.2,
        "requires_commerce": 0.4, "requires_tech": 0.8,
        "tags": ["data", "statistics", "AI", "coding", "analytics"]
    },
    {
        "name": "Medicine (MBBS)",
        "field": "science",
        "description": "Study of human body, diseases, diagnosis, and treatment.",
        "requires_math": 0.5, "requires_science": 1.0, "requires_arts": 0.4,
        "requires_commerce": 0.1, "requires_tech": 0.5,
        "tags": ["health", "biology", "patient care", "research", "science"]
    },
    {
        "name": "Architecture",
        "field": "arts",
        "description": "Design of buildings and spaces combining art, science, and engineering.",
        "requires_math": 0.7, "requires_science": 0.5, "requires_arts": 0.9,
        "requires_commerce": 0.2, "requires_tech": 0.6,
        "tags": ["design", "creativity", "construction", "spatial", "drawing"]
    },
    {
        "name": "Economics",
        "field": "commerce",
        "description": "Study of markets, finance, policy, and resource allocation.",
        "requires_math": 0.8, "requires_science": 0.3, "requires_arts": 0.5,
        "requires_commerce": 0.8, "requires_tech": 0.4,
        "tags": ["finance", "policy", "markets", "analysis", "business"]
    },
    {
        "name": "Fine Arts & Design",
        "field": "arts",
        "description": "Creative expression through visual art, digital design, and media.",
        "requires_math": 0.1, "requires_science": 0.1, "requires_arts": 1.0,
        "requires_commerce": 0.2, "requires_tech": 0.4,
        "tags": ["creativity", "design", "art", "visual", "media"]
    },
    {
        "name": "Biotechnology",
        "field": "science",
        "description": "Application of biology and technology in medicine, agriculture, and industry.",
        "requires_math": 0.6, "requires_science": 0.9, "requires_arts": 0.2,
        "requires_commerce": 0.2, "requires_tech": 0.7,
        "tags": ["biology", "research", "health", "technology", "science"]
    },
]


# ─── Scoring Helpers ──────────────────────────────────────────────────────────

def _aptitude_score(profile: UserProfile, degree: Dict) -> float:
    """
    Content-based score: how well the user's aptitude matches degree requirements.
    Uses weighted cosine-like dot product normalized to [0, 1].
    """
    user_vec = [
        profile.math_score,
        profile.science_score,
        profile.arts_score,
        profile.commerce_score,
        profile.tech_score,
    ]
    degree_vec = [
        degree["requires_math"],
        degree["requires_science"],
        degree["requires_arts"],
        degree["requires_commerce"],
        degree["requires_tech"],
    ]

    dot = sum(u * d for u, d in zip(user_vec, degree_vec))
    magnitude = sum(d ** 2 for d in degree_vec) ** 0.5
    return dot / (magnitude * len(user_vec)) if magnitude else 0.0


def _interest_overlap_score(profile: UserProfile, degree: Dict) -> float:
    """
    Content-based score: how many of the user's interests match degree tags.
    Returns fraction of degree tags matched (0.0 - 1.0).
    """
    user_interests = set(i.lower() for i in (profile.interests or []))
    degree_tags = set(t.lower() for t in degree.get("tags", []))

    if not degree_tags:
        return 0.0
    overlap = user_interests & degree_tags
    return len(overlap) / len(degree_tags)


def _field_preference_score(profile: UserProfile, degree: Dict) -> float:
    """Bonus score if user explicitly prefers this field."""
    preferred = [f.lower() for f in (profile.preferred_fields or [])]
    return 1.0 if degree["field"].lower() in preferred else 0.0


def _work_style_score(profile: UserProfile, degree: Dict) -> float:
    """
    Simulated collaborative filtering: users with similar work_style
    tend to prefer certain fields. Maps work style to field affinity.
    """
    style_field_map = {
        "analytical": {"engineering": 1.0, "science": 0.8, "commerce": 0.5, "arts": 0.2},
        "creative":   {"arts": 1.0, "engineering": 0.5, "science": 0.4, "commerce": 0.3},
        "mixed":      {"engineering": 0.7, "arts": 0.7, "science": 0.6, "commerce": 0.6},
    }
    style = (profile.work_style or "mixed").lower()
    field_affinities = style_field_map.get(style, style_field_map["mixed"])
    return field_affinities.get(degree["field"].lower(), 0.5)


def _build_match_reason(profile: UserProfile, degree: Dict, scores: Dict) -> str:
    """Generate a short human-readable explanation for the recommendation."""
    reasons = []

    if scores["aptitude"] > 0.6:
        reasons.append("your aptitude aligns well with this degree's requirements")
    if scores["interest"] > 0.3:
        matched = set(i.lower() for i in profile.interests) & set(t.lower() for t in degree["tags"])
        reasons.append(f"your interests ({', '.join(matched)}) match this field")
    if scores["field_pref"] > 0:
        reasons.append(f"you prefer the {degree['field']} field")
    if scores["work_style"] > 0.7:
        reasons.append(f"suits your {profile.work_style} work style")

    if not reasons:
        return "General match based on your profile."
    return "Recommended because " + "; ".join(reasons) + "."


# ─── Main Engine ─────────────────────────────────────────────────────────────

WEIGHTS = {
    "aptitude": 0.40,
    "interest": 0.30,
    "field_pref": 0.20,
    "work_style": 0.10,
}


def generate_recommendations(profile: UserProfile, top_n: int = 5) -> List[Dict]:
    """
    Hybrid recommendation engine.
    Combines content-based filtering (aptitude + interests + field preference)
    with simulated collaborative filtering (work style mapping).
    Returns top_n ranked degree recommendations.
    """
    results = []

    for degree in DEGREE_CATALOG:
        scores = {
            "aptitude":   _aptitude_score(profile, degree),
            "interest":   _interest_overlap_score(profile, degree),
            "field_pref": _field_preference_score(profile, degree),
            "work_style": _work_style_score(profile, degree),
        }

        # Weighted final score
        final_score = sum(WEIGHTS[k] * v for k, v in scores.items())

        results.append({
            "degree_name":   degree["name"],
            "field":         degree["field"],
            "description":   degree["description"],
            "score":         round(final_score, 4),
            "match_reason":  _build_match_reason(profile, degree, scores),
        })

    # Sort descending by score, return top N
    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:top_n]
