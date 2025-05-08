import json
from utils import get_links_from_homepage

with open('config.json', 'r') as file:
    config = json.load(file)

if __name__ == "__main__":
    url = config["url"]
    css_selector = config["css_selector"]
    get_links_from_homepage(url, css_selector)
