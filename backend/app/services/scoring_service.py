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