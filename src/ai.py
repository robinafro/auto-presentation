import dotenv, requests, os
from openai import OpenAI
from settings import KEY_ENV_NAME, ROTATOR_URL, SYSPROMPT_PATH, RESPONSE_CACHE_PATH, MODEL, MODEL_TEMPERATURE

dotenv.load_dotenv()

def fetch_key():
    # Get the value of KEY_ENV_NAME in .env
    stuckinvim_key = os.environ.get(KEY_ENV_NAME)

    assert stuckinvim_key != None, f"Please set {KEY_ENV_NAME} in the .env to your key rotator key!"

    # Fetch the actual open ai key
    response = requests.get(ROTATOR_URL.replace("%key%", stuckinvim_key))
    
    assert response.status_code == 200, "Invalid key rotator key!"
    assert response.json().get("key", None) != None, "Key rotator returned invalid response!"

    return response.json()["key"]

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

def get_response(client, prompt, debug_cache=False):
    # If the debug cache is enabled, use it instead of wasting tokens
    if debug_cache and os.path.exists(RESPONSE_CACHE_PATH):
        with open(RESPONSE_CACHE_PATH, "r") as f:
            return f.read()

    messages = [
        {"role": "user", "content": prompt}
    ]

    chat_completion = client.chat.completions.create(
        messages=messages,
        model=MODEL,
        temperature=MODEL_TEMPERATURE,
    )

    text = chat_completion.choices[0].message.content

    with open(RESPONSE_CACHE_PATH, "w") as f:
        f.write(text)

    return text

def create_client():
    return OpenAI(
        api_key=fetch_key()
    )

if __name__ == "__main__":
    client = OpenAI(
        api_key=fetch_key()
    )

    prompt = fill_sysprompt(subject="Martin Luther King", country="the Czech Republic", language="czech", num_slides="4")

    response = get_response(client, prompt, debug_cache=True)

    print(response)
