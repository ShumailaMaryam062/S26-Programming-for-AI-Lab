STAGE_SCHEMAS = {
    "ats": {
        "keys": ["ats_score", "breakdown", "strengths", "weaknesses", "final_summary"],
        "fallback": {
            "ats_score": "N/A",
            "breakdown": {},
            "strengths": [],
            "weaknesses": [],
            "final_summary": "",
        },
    },
    "improvements": {
        "keys": [
            "headline_improvements",
            "formatting_improvements",
            "content_improvements",
            "keyword_optimization",
            "bullet_point_improvements",
            "priority_actions",
        ],
        "fallback": {
            "headline_improvements": [],
            "formatting_improvements": [],
            "content_improvements": [],
            "keyword_optimization": [],
            "bullet_point_improvements": [],
            "priority_actions": [],
        },
    },
    "skill_gap": {
        "keys": [
            "present_skills",
            "missing_skills",
            "critical_gaps",
            "priority_skills_to_learn",
            "market_alignment",
            "recommendation_level",
        ],
        "fallback": {
            "present_skills": [],
            "missing_skills": [],
            "critical_gaps": [],
            "priority_skills_to_learn": [],
            "market_alignment": "",
            "recommendation_level": "",
        },
    },
    "career_paths": {
        "keys": ["top_paths", "final_recommendation"],
        "fallback": {"top_paths": [], "final_recommendation": ""},
    },
    "roadmap": {
        "keys": [
            "phase_1_fundamentals",
            "phase_2_core_projects",
            "phase_3_advanced_internship_prep",
            "final_outcome",
            "career_readiness_level",
        ],
        "fallback": {
            "phase_1_fundamentals": {},
            "phase_2_core_projects": {},
            "phase_3_advanced_internship_prep": {},
            "final_outcome": "",
            "career_readiness_level": "",
        },
    },
}


NEXT_STAGE = {
    "ats": "improvements",
    "improvements": "skill_gap",
    "skill_gap": "career_paths",
    "career_paths": "roadmap",
}

