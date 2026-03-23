
def parse_chat_input(message: str) -> dict:
    """
    Parse the user's chat message to extract profile update signals.
    In production, this can be replaced with an NLP model or LLM call.
    """
    msg = message.lower()
    updates = {}
    reply_hints = []

    # Detect interest keywords
    interest_keywords = {
        "coding": ["coding", "programming", "code", "software", "developer"],
        "design": ["design", "creative", "art", "draw", "visual"],
        "data": ["data", "analytics", "statistics", "numbers"],
        "health": ["health", "medicine", "biology", "doctor", "patient"],
        "business": ["business", "management", "finance", "marketing", "entrepreneur"],
        "research": ["research", "science", "experiment", "lab"],
        "teaching": ["teaching", "education", "learn", "students"],
        "machines": ["machines", "mechanical", "robot", "build", "construct"],
    }

    detected_interests = []
    for interest, keywords in interest_keywords.items():
        if any(kw in msg for kw in keywords):
            detected_interests.append(interest)
    if detected_interests:
        updates["interests"] = detected_interests
        reply_hints.append(f"interests in {', '.join(detected_interests)}")

    # Detect work style preference
    if any(w in msg for w in ["creative", "artistic", "imagination", "design"]):
        updates["work_style"] = "creative"
        reply_hints.append("creative work style")
    elif any(w in msg for w in ["analytical", "logical", "math", "numbers", "data"]):
        updates["work_style"] = "analytical"
        reply_hints.append("analytical work style")

    # Detect field preference
    field_keywords = {
        "engineering": ["engineering", "tech", "computer", "software", "hardware"],
        "science": ["science", "biology", "chemistry", "medicine", "physics"],
        "arts": ["arts", "humanities", "psychology", "literature", "design"],
        "commerce": ["commerce", "business", "economics", "finance", "management"],
    }
    preferred_fields = []
    for field, keywords in field_keywords.items():
        if any(kw in msg for kw in keywords):
            preferred_fields.append(field)
    if preferred_fields:
        updates["preferred_fields"] = preferred_fields
        reply_hints.append(f"preference for {', '.join(preferred_fields)}")

    # Build reply
    if reply_hints:
        reply = f"Got it! I've updated your profile based on your {' and '.join(reply_hints)}. Here are your refreshed recommendations:"
    else:
        reply = "Thanks for the input! I've noted your feedback. Here are your current recommendations:"

    return {"updates": updates, "reply": reply}
