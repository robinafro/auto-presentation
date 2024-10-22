import requests, os
from settings import (
    KEY_ENV_NAME,
    ROTATOR_URL,
    SYSPROMPT_PATH,
    RESPONSE_CACHE_PATH,
    MODEL,
    MODEL_TEMPERATURE,
)


def fill_sysprompt(**kwargs):
    # Read the system prompt from its path
    with open(SYSPROMPT_PATH, "r") as f:
        sysprompt = f.read()

    # Replace all occurences of each key with the value associated with it
    for key, value in kwargs.items():
        key_processed = f"%{key}%"

        assert key_processed in sysprompt, f"Key {key} not found in system prompt!"

        sysprompt = sysprompt.replace(key_processed, str(value))

    return sysprompt
