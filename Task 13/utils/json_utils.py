import json

from prompts.stage_schemas import STAGE_SCHEMAS


def parse_model_json(text, stage):
    fallback = dict(STAGE_SCHEMAS[stage]["fallback"])
    try:
        payload = json.loads(text)
        if not isinstance(payload, dict):
            return fallback
        for key in STAGE_SCHEMAS[stage]["keys"]:
            if key in payload:
                fallback[key] = payload[key]
        return fallback
    except Exception:
        fallback["raw_response"] = text
        return fallback

