import re
from typing import List, Dict

def get_all_links(content: str) -> List[str]:
    """
    Extract all links from the markdown content, excluding those that contain the word "video".

    Args:
        content (str): The Markdown content as a string.

    Returns:
        List[str]: A list of URL links.
    """
    # Find all markdown links
    markdown_links = re.findall(r"\[.*?\]\(https?://[^\s)]+\)", content)

    # Filter out links containing the word "video"
    filtered_links = [
        re.search(r'https?://[^\)]+', link).group(0)
        for link in markdown_links
        if "video" not in re.search(r"\((.*?)\)", link).group(1).lower()
    ]

    return filtered_links


def extract_links_from_markdown(content: str) -> List[Dict[str, str]]:
    """
    Extract all links from the markdown content as {'text': ..., 'url': ...},
    excluding image links.

    Args:
        content (str): The Markdown content as a string.

    Returns:
        List[Dict[str, str]]: A list of dictionaries containing {'text': ..., 'url': ...}.
    """
    # Remove image links
    image_link_pattern = r'\[ !\[.*?\]\(.*?\)\s.*?\]\(.*?\)'
    content_no_images = re.sub(image_link_pattern, '', content)

    # Find all non-image links
    link_pattern = re.compile(r'(?<!\!)\[(.*?)\]\((https?://[^\s)]+)\)')
    links = {
        (match.group(1).strip(), match.group(2).strip())
        for match in link_pattern.finditer(content_no_images)
    }

    # Return a list of dictionaries with 'text' and 'url'
    return [{"text": text, "url": url} for text, url in links]
