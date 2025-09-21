import pytest
from unittest.mock import MagicMock, patch
from utils import utils
from .engine import ResultFetcher
from .search_wiki import WikiSearch
from .ai_helper import AIHelper

@pytest.fixture
def aihelper():
    return AIHelper()

@pytest.fixture
def resultfetcher():
    return ResultFetcher()

def test_ai_helper_Python(aihelper):
    assert utils.extract_category_or_article(aihelper.is_wiki_or_fandom("Пайтон")) == "wiki"
    assert utils.extract_category_or_article(aihelper.is_category_or_article("Пайтон")) == "article"
    assert utils.extract_category_or_article(aihelper.get_wiki_article("Пайтон")) == "Python (programming language)"

def test_ai_helper_ICB(aihelper):
    assert utils.extract_category_or_article(aihelper.is_wiki_or_fandom("Бренды мороженого")) == "wiki"
    assert utils.extract_category_or_article(aihelper.is_category_or_article("Бренды мороженого")) == "category"
    assert utils.extract_category_or_article(aihelper.get_wiki_category("Бренды мороженого")) == "Category:Ice cream brands"

def test_engine_python(resultfetcher):
    resultfetcher.set_theme("Пайтон")
    print(resultfetcher.get())


def test_engine_icb(resultfetcher):
    resultfetcher.set_theme("Бренды мороженого")
    print(resultfetcher.get())


def test_engine_silksong(resultfetcher):
    resultfetcher.set_theme("Силксонг")
    print(resultfetcher.get())
