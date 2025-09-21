from . import ai_helper
from . import file_creator
from search_engine.search_fandom import FandomSearch
from utils import utils, config
from .search_wiki import WikiSearch
from pathlib import Path

class ResultFetcher:
    def __init__(self, theme: str = None):
        self.theme = theme
        self.file_creator = file_creator.FileCreator(root=Path(__file__).resolve().parent.parent / "files")
        self.ai = ai_helper.AIHelper()

    def set_theme(self, theme: str):
        self.theme = theme

    def get(self) -> list[str] | Exception | list[Path]:
        try:
            source = utils.extract_category_or_article(
                self.ai.is_wiki_or_fandom(self.theme)
            ).lower()

            if source == "wiki":
                return self._get_wiki()
            return self._get_fandom()
        except Exception as e:
            return e

    def _get_fandom(self):
        kind = utils.extract_category_or_article(
            self.ai.is_wiki_category_or_article(self.theme)
        ).lower()

        client = FandomSearch(
            f"{config.PROJECT_NAME} ({config.EMAIL})",
            utils.extract_category_or_article(self.ai.from_what_wiki_theme(self.theme)),
            "en",
        )

        if kind == "wiki":
            return self._process_fandom_pages(client.get_all_pages(), client)

        if kind == "category":
            return self._process_fandom_pages(client.get_category_pages(self.theme), client)

        page = client.page(self.ai.get_article_page(self.theme))
        return [page.summary, page.plain_text]

    def _process_fandom_pages(self, pages_titles, client):
        for title in pages_titles:
            page = client.page(title)
            self.file_creator.add_file(page.title, page.plain_text)
        output_paths = self.file_creator.create_archives()
        return output_paths

    def _get_wiki(self):
        kind = utils.extract_category_or_article(
            self.ai.is_category_or_article(self.theme)
        )

        wiki = WikiSearch()

        if kind == "article":
            article = utils.extract_category_or_article(self.ai.get_wiki_article(self.theme))
            return wiki.get_text(article.replace(" ", "_"))

        category = utils.extract_category_or_article(self.ai.get_wiki_category(self.theme))
        articles = wiki.collect_all_articles(category.replace(" ", "_"))

        for article in articles:
            text = wiki.get_text(article)
            self.file_creator.add_file(article, text)

        output_paths = self.file_creator.create_archives()
        return output_paths

    def cleanup(self):
        self.file_creator.cleanup()
