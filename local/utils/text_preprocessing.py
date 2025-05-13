import re
from typing import List, Dict

def get_all_links(content: str) -> List[str]:
    """
    Extract all URL links from the given markdown content, excluding any links that contain the word "video".

    Description:
    -----------
    This function uses regular expressions to find all standard markdown-style links 
    in the content (e.g., `[title](http://example.com)`). It then filters out links
    whose URLs contain the word "video", making it useful for extracting only 
    readable or article links.

    Parameters:
    ----------
    content : str
        A string containing markdown-formatted text.

    Returns:
    -------
    List[str]
        A list of raw URL strings extracted from the markdown content.

    Example:
    --------
    >>> get_all_links("This is a [link](http://example.com) and [video](http://example.com/video)")
    ['http://example.com']
    """
    markdown_links = re.findall(r"\[.*?\]\(https?://[^\s)]+\)", content)

    filtered_links = [
        re.search(r'https?://[^\)]+', link).group(0)
        for link in markdown_links
        if "video" not in re.search(r"\((.*?)\)", link).group(1).lower()
    ]

    return filtered_links

def extract_links_from_markdown(content: str) -> List[Dict[str, str]]:
    """
    Extract all standard (non-image) markdown links and return them as a list of dictionaries
    containing the link text and URL.

    Description:
    -----------
    This function first removes embedded image links, then uses a regular expression
    to extract remaining markdown links with the format `[title](url)`. It avoids
    links prefixed with `!` (image links). The results are returned as a list of 
    dictionaries with `title` and `url` keys.

    Parameters:
    ----------
    content : str
        The markdown-formatted text from which to extract links.

    Returns:
    -------
    List[Dict[str, str]]
        A list of dictionaries in the form: {"title": ..., "url": ...}.

    Example:
    --------
    >>> extract_links_from_markdown("Visit [Google](https://google.com).")
    [{'title': 'Google', 'url': 'https://google.com'}]
    """
    image_link_pattern = r'\[ !\[.*?\]\(.*?\)\s.*?\]\(.*?\)'
    content_no_images = re.sub(image_link_pattern, '', content)

    link_pattern = re.compile(r'(?<!\!)\[(.*?)\]\((https?://[^\s)]+)\)')
    links = {
        (match.group(1).strip(), match.group(2).strip())
        for match in link_pattern.finditer(content_no_images)
    }

    return [{"title": title, "url": url} for title, url in links]

def merge_in_one_paragraph(content: str) -> str:
    """
    Merge all lines and paragraphs from the markdown content into a single paragraph.

    Description:
    -----------
    This utility function removes all newlines and excessive whitespace from the text,
    effectively combining multi-line or multi-paragraph content into a single continuous
    paragraph. This is helpful for summarization or NLP preprocessing tasks.

    Parameters:
    ----------
    content : str
        The markdown or plain text content to be merged.

    Returns:
    -------
    str
        A single paragraph string with normalized spacing.

    Example:
    --------
    >>> merge_in_one_paragraph("Line one.\nLine two.\n\nLine three.")
    'Line one. Line two. Line three.'
    """
    return re.sub(r'\s+', ' ', content).strip()
