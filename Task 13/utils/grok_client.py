import os

import requests

import config
from prompts.stage_schemas import STAGE_SCHEMAS
from prompts.system_prompts import SYSTEM_PROMPTS
from utils.json_utils import parse_model_json
from utils.text_utils import clean_prompt_text, normalize_prompt_text


def build_user_prompt(stage, resume_text, extra=None):
    schema_keys = STAGE_SCHEMAS[stage]["keys"]
    extra = extra or {}

    if stage == "career_paths":
        interests = str(extra.get("interests") or "").strip()
        goal = str(extra.get("goal") or "").strip()
        context = str(extra.get("retrieved_context") or "").strip()
        return (
            "Recommend career paths using the retrieved context. Return ONLY valid JSON with exactly these top-level keys: "
            + ", ".join(schema_keys)
            + ".\n\n"
            + "If Interests/Goal are not provided, infer them from the resume.\n\n"
            + "Interests: %s\n" % (interests or "Not provided (infer from resume)")
            + "Goal: %s\n\n" % (goal or "Not provided (infer from resume)")
            + "Retrieved Context:\n%s\n\n" % (context or "No context available")
            + "Resume:\n%s" % resume_text
        )

    return (
        "Analyze the following resume for stage '%s'. " % stage
        + "Return ONLY valid JSON with exactly these top-level keys: "
        + ", ".join(schema_keys)
        + ".\n\nResume:\n%s" % resume_text
    )


def call_grok(stage, resume_text, extra=None):
    api_key = config.GROK_API_KEY
    if not api_key:
        raise RuntimeError("Missing GROK_API_KEY environment variable.")

    api_url = config.GROK_API_URL or config.GROK_BASE_URL or os.getenv("GROK_BASe_URL", "")
    if not api_url:
        raise RuntimeError("Missing API base URL. Set GROK_API_URL or GROK_BASE_URL.")

    model_name = config.GROK_MODEL
    if not model_name:
        raise RuntimeError("Missing GROK_MODEL environment variable.")

    normalized_url = api_url.rstrip("/")
    if not normalized_url.endswith("/chat/completions"):
        normalized_url = normalized_url + "/chat/completions"

    response = requests.post(
        normalized_url,
        headers={
            "Authorization": "Bearer %s" % api_key,
            "Content-Type": "application/json",
        },
        json={
            "model": model_name,
            "messages": [
                {
                    "role": "system",
                    "content": clean_prompt_text(normalize_prompt_text(SYSTEM_PROMPTS[stage])),
                },
                {"role": "user", "content": build_user_prompt(stage, resume_text, extra=extra)},
            ],
            "temperature": 0.2,
        },
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()
    content = data["choices"][0]["message"]["content"]
    return parse_model_json(content, stage)
