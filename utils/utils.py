import re
from urllib.parse import urlparse
import logger

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