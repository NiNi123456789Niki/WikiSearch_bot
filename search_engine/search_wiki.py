from utils import logger
import wikipediaapi
from utils.config import PROJECT_NAME, EMAIL
from collections import deque
import time


class WikiSearch:
    def __init__(self, language: str = "en"):
        self.client = wikipediaapi.Wikipedia(
            user_agent=f"{PROJECT_NAME} ({EMAIL})",
            language=language,
            extract_format=wikipediaapi.ExtractFormat.WIKI,
        )

    def get_page(self, title: str):
        return self.client.page(title)

    def check_page(self, title: str) -> bool:
        return self.get_page(title).exists()

    def get_text(self, title: str):
        if self.check_page(title):
            page = self.get_page(title)
            return [page.summary, page.text]
        return None

    def collect_all_articles(self, category_title: str):
        logger.log("DEBUG", category_title)
        category_page = self.get_page(category_title)
        visited_categories = set()
        articles = []
        queue = deque([category_page])

        while queue:
            current_cat = queue.popleft()
            if current_cat.title in visited_categories:
                continue
            visited_categories.add(current_cat.title)

            for c in current_cat.categorymembers.values():
                if c.ns == wikipediaapi.Namespace.CATEGORY:
                    queue.append(c)
                elif c.ns == wikipediaapi.Namespace.MAIN:
                    articles.append(c.title)

            time.sleep(10)

        return articles
