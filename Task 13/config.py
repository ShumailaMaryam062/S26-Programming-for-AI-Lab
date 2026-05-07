import os


def get_env(name, default=""):
    value = os.getenv(name)
    if value is None:
        return default
    return value


DATA_DIR = get_env("DATA_DIR", "data")
KB_DIR = get_env("KB_DIR", "kb")
GROK_API_KEY = get_env("GROK_API_KEY", "")
GROK_API_URL = get_env("GROK_API_URL", "")
GROK_BASE_URL = get_env("GROK_BASE_URL", "")
GROK_MODEL = get_env("GROK_MODEL", "")

