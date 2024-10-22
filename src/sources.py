from googlesearch import search
import re

def parse_source_tags(md):
    all_matches = re.findall(r"source://'(.*?)'", md)

    for match in all_matches:
        print(match)
        for link in search(match, num=1, stop=1, pause=0):
            print(link)
            md = md.replace(f"source://'{match}'", link)

    return md

if __name__ == "__main__":
    from settings import RESPONSE_CACHE_PATH

    with open(RESPONSE_CACHE_PATH, "r") as f:
        md = f.read()
        print(parse_source_tags(md))

