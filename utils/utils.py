import re
from urllib.parse import urlparse
from . import logger

def get_page_title(text):
    match = re.search(r'https?://\S+', text)
    if match:
        url = match.group(0)
        path = urlparse(url).path
        title = path.split("/wiki/")[-1]
        logger.log("INFO", title)
        return title
    logger.log("WARN", "No page title found")
    return None


def extract_category_or_article(text: str) -> str:
    match = re.search(r"\*\*(.+?)\*\*", text)
    if match:
        item = match.group(1).strip()
    else:
        item = text.strip()

    return item