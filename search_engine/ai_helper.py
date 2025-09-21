from utils import logger, config
from google import genai


class AIHelper:
    def __init__(self, api_key: str = None):
        self.client = genai.Client(api_key=api_key or config.GEMINI_API)

    def _ask(self, prompt: str) -> str:
        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt + " anwser on English",
        )
        logger.log("DEBUG", response.text)
        return response.text.strip()

    def is_category_or_article(self, theme: str) -> str:
        answer = self._ask(
            f"{theme} - is category or article on Wikipedia? Say one word: small 'article' or 'category'"
        )
        return "article" if "article" in answer.lower() else "category"

    def get_text_with_url(self, theme: str) -> str:
        return self._ask(f"return link of page {theme} on Wikipedia")

    def get_wiki_category(self, category: str) -> str:
        return self._ask(
            f"{category} - what is name of this category on En Wikipedia, return only 100% correct name? With 'Category:', like 'Category:Physics'"
        )

    def get_wiki_article(self, article: str) -> str:
        return self._ask(
            f"{article} - what is name of this article on En Wikipedia, return only 100% correct full name?"
        )

    def is_wiki_or_fandom(self, theme: str) -> str:
        return self._ask(
            f"{theme} - where is better to see this theme in fandom.com or wikipedia? Say one word: small 'wiki' or 'fandom' (if this is game always anwser fandom)"
        )

    def is_wiki_category_or_article(self, theme: str) -> str:
        return self._ask(
            f"{theme} - This is fandom.com wiki, category or article? Say one word: small 'wiki', 'category' or 'article'"
        )

    def get_wiki(self, wiki: str) -> str:
        return self._ask(
            f"{wiki} - what is name of this wiki page on fandom.com? return only 100% correct name"
        )

    def get_category_fandom(self, category: str) -> str:
        return self._ask(
            f"{category} - what is name of this category page on fandom.com? return only 100% correct name"
        )

    def get_article_page(self, article: str) -> str:
        return self._ask(
            f"{article} - what is name of this article page on fandom.com? return only 100% correct name"
        )

    def from_what_wiki_theme(self, theme: str) -> str:
        return self._ask(
            f"{theme} - what is name of the wiki of this page on fandom.com? return only 100% correct name"
        )
