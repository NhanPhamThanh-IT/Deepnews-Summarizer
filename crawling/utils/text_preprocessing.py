import re

def get_all_links(content):
    markdown_links = re.findall(r"\[.*?\]\(https?://[^\s)]+\)", content)

    filtered_links = [
        re.search(r'https?://[^\)]+', link).group(0) for link in markdown_links
        if "video" not in re.search(r"\((.*?)\)", link).group(1).lower()
    ]

    return filtered_links
