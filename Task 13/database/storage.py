import json
import os

import config



resume_store = {}


def ensure_data_dir():
    os.makedirs(config.DATA_DIR, exist_ok=True)


def analysis_file_path(analysis_id):
    ensure_data_dir()
    return os.path.join(config.DATA_DIR, "analysis_%s.json" % analysis_id)


def save_analysis_state(analysis_id, state):
    path = analysis_file_path(analysis_id)
    tmp_path = "%s.tmp" % path
    with open(tmp_path, "w", encoding="utf-8") as handle:
        json.dump(state, handle, ensure_ascii=False, indent=2)
    os.replace(tmp_path, path)


def load_analysis_state(analysis_id):
    path = analysis_file_path(analysis_id)
    if not os.path.exists(path):
        return None
    try:
        with open(path, "r", encoding="utf-8") as handle:
            payload = json.load(handle)
        if not isinstance(payload, dict):
            return None
        if "resume_text" not in payload or "results" not in payload:
            return None
        return payload
    except Exception:
        return None


def get_or_load_state(analysis_id):
    state = resume_store.get(analysis_id)
    if state:
        return state
    disk_state = load_analysis_state(analysis_id)
    if disk_state:
        resume_store[analysis_id] = disk_state
        return disk_state
    return None

