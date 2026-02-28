def calculate_score(candidate: dict, job_skills: list) -> float:

    if not job_skills:
        return 0.0

    candidate_skills = [skill.lower() for skill in candidate.get("skills", [])]
    required_skills = [skill.lower() for skill in job_skills]

    matched = len(set(candidate_skills) & set(required_skills))
    skill_ratio = matched / len(required_skills)

    experience = candidate.get("experience", 0)
    exp_ratio = min(experience / 5, 1)  # cap at 5 years

    education = candidate.get("education", 0)

    final_score = (
        (skill_ratio * 0.5) +
        (exp_ratio * 0.3) +
        (education * 0.2)
    )

    return round(final_score, 2)


def rank_candidates(candidates: list, job_skills: list) -> list:

    ranked = []

    for candidate in candidates:
        score = calculate_score(candidate, job_skills)

        updated_candidate = candidate.copy()
        updated_candidate["score"] = score

        ranked.append(updated_candidate)

    return sorted(ranked, key=lambda x: x["score"], reverse=True)