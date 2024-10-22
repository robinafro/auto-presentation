from settings import MARP_DOWNLOAD_URL, MARP_DOWNLOAD_DIR, MARP_INSTALL_DIR
import requests, tarfile, shutil, os
import subprocess

def install_marp():
    # Download marp or find cached version
    print("Downloading Marp...")

    content = None
    if os.path.exists(os.path.join(MARP_DOWNLOAD_DIR, "marp.tar.gz")):
        with open(os.path.join(MARP_DOWNLOAD_DIR, "marp.tar.gz"), "rb") as f:
            content = f.read()

    if content is None or len(content) == 0:
        try:
            content = requests.get(MARP_DOWNLOAD_URL).content
            print("Marp downloaded successfully.")
        except requests.exceptions.RequestException as e:
            print(f"Failed to download Marp: {e}")
            return
    else:
        print("Marp already downloaded")

    with open(os.path.join(MARP_DOWNLOAD_DIR, "marp.tar.gz"), "wb") as f:
        f.write(content)

    # Extract (tar.gz)
    with tarfile.open(os.path.join(MARP_DOWNLOAD_DIR, "marp.tar.gz"), "r:gz") as tar:
        tar.extractall()

    print("Marp extracted successfully. Cleaning up...")

    # Move the marp binary to the bin directory from the MARP_DOWNLOAD_PATH
    if not os.path.exists(MARP_INSTALL_DIR):
        os.makedirs(MARP_INSTALL_DIR)

    shutil.move(os.path.join(os.path.dirname(os.path.dirname(__file__)), "marp"), MARP_INSTALL_DIR)

def is_installed():
    return os.path.exists(os.path.join(MARP_INSTALL_DIR, "marp"))

def marp_convert(input_path, output_path, options: str):
    if not is_installed():
        print("Marp is not installed. Installing...")
        install_marp()

    marp = os.path.join(MARP_INSTALL_DIR, "marp")
    status = subprocess.run([marp, input_path, "-o", output_path, options])

    assert status.returncode == 0, f"Failed to convert {input_path} to {output_path}"

    print(f"Converted {input_path} to {output_path}")

if __name__ == "__main__":
    marp_convert("test.md", "test.pptx", "--pptx")
