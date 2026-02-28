def calculate_score(candidate, job_skills):

    if not job_skills:
        return 0

    skill_match = len(
        set(candidate["skills"]) &
        set(job_skills)
    ) / len(job_skills)

    exp_score = candidate["experience"] * 0.1
    edu_score = candidate["education"]

    score = (skill_match*0.5) + (exp_score*0.3) + (edu_score*0.2)

    return round(score,2)


def rank_candidates(candidates, job_skills):

    for c in candidates:
        c["score"] = calculate_score(c, job_skills)

    return sorted(candidates, key=lambda x:x["score"], reverse=True)