from utils import logger
from utils import config
from google import genai

client = genai.Client(api_key=config.GEMINI_API)

def send(text):
    response = client.models.generate_content(
        model="gemini-2.5-flash", contents=text
    )
    if response.error_message:
        logger.log("ERROR", response.error_message)
    else:
        logger.log("INFO", response.content)
    return response.content

def is_category_or_article(theme):
    answer = send(f"{theme} - is category or article")
    if "article" in answer:
        return "article"
    else:
        return "category"

def get_text_with_url(theme):
    return send(f"return link of page {theme} on Wikipedia")

def get_wiki_category(category):
    return send(f"{category} - what is name of this on En Wikipedia?")