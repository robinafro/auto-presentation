import os

# Images
IMAGE_WHITELIST = [
    "jpg",
    "jpeg",
    "png"
]

# Keys
KEY_ENV_NAME = "STUCKINVIM_KEY"
ROTATOR_URL = "http://getkey.stuckinvim.com/api/data?api_key=%key%"

# AI
SYSPROMPT_PATH = os.path.join(os.path.dirname(__file__), "prompts", "prompt.txt")
RESPONSE_CACHE_PATH = os.path.join(os.path.dirname(__file__), "cache.txt")
MODEL="gpt-4o-mini"
MODEL_TEMPERATURE=0.6

# Marp
MARP_DOWNLOAD_URL = "https://github.com/marp-team/marp-cli/releases/download/v3.4.0/marp-cli-v3.4.0-linux.tar.gz"
MARP_DOWNLOAD_DIR = "/tmp/"
MARP_INSTALL_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "bin")

# Generator
MD_STORE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "md")
PPTX_STORE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "pptx")
