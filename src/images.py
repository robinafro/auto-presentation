import requests, re
from bing_image_urls import bing_image_urls
from settings import IMAGE_WHITELIST

def fetch_images_from_query(query):
    urls = bing_image_urls(query)

    return urls

def is_valid(image_url):
    extension = image_url.split('.')[-1]

    if extension not in IMAGE_WHITELIST:
        return False

    try:
        response = requests.get(image_url, timeout=3)

        assert response.status_code == 200, "Invalid status code!"
    except:
        return False

    return True

def choose_valid_image(query):
    images = fetch_images_from_query(query)

    for image in images:
        if is_valid(image):
            return image.replace(" ", "%20")

    return ""

def parse_img_tags(md):
    # Takes in the produced markdown, finds all "query://'query here'" (not including the outer double quotes, only the inner ones), returns the queries (for example "query here")
    all_matches = re.findall(r"query://'(.*?)'", md)

    for match in all_matches:
        # Replace all the "query://''" with the image url
        md = md.replace(f"query://'{match}'", choose_valid_image(match))

    return md

if __name__ == "__main__":
    from settings import RESPONSE_CACHE_PATH
    
    with open(RESPONSE_CACHE_PATH, "r") as f:
        md = f.read()
        print(parse_img_tags(md))
