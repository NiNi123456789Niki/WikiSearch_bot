import wikipediaapi
from utils.config import PROJECT_NAME, EMAIL
from collections import deque

wiki_wiki = wikipediaapi.Wikipedia(
    user_agent=f'{PROJECT_NAME} ({EMAIL})',
    language='en',
    extract_format=wikipediaapi.ExtractFormat.WIKI
)

def get_page(title):
    return wiki_wiki.page(title)

def check_page(title):
    return get_page(title).exists()

def get_text_page(title):
    if check_page(title):
        return get_page(title).text
    return None

def collect_all_articles(category_page):
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

    return articles


