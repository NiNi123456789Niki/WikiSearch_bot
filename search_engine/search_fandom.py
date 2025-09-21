import fandom
import requests
from utils import logger

class FandomSearch:
    def __init__(self, us_agent: str, wiki="", language="en"):
        self.wiki = wiki
        self.language = language
        self.us_agent = us_agent
        self.url = "https://" + wiki + ".fandom.com/"
        self.session = requests.Session()
        self.set_fandom_lib()
        logger.log("DEBUG", f"Initialized FandomSearch for wiki: {wiki}, language: {language}")

    def set_wiki(self, wiki):
        self.wiki = wiki
        self.url = "https://" + wiki + ".fandom.com/"
        fandom.set_wiki(self.wiki)
        logger.log("DEBUG", f"Wiki changed to: {wiki}")

    def set_fandom_lib(self):
        fandom.set_user_agent(self.us_agent)
        fandom.set_lang(self.language)
        logger.log("DEBUG", f"Fandom lib configured: user_agent={self.us_agent}, language={self.language}")

    def page(self, title):
        logger.log("DEBUG", f"Fetching page: {title}")
        p = fandom.page(title)
        logger.log("DEBUG", f"Page fetched: {title}")
        return p

    def get_all_pages(self):
        api_url = self.url + "api.php"
        session = self.session
        params = {
            "action": "query",
            "list": "allpages",
            "aplimit": "50",
            "format": "json"
        }

        cont = True
        apcontinue = None

        while cont:
            if apcontinue:
                params["apcontinue"] = apcontinue
            logger.log("DEBUG", f"Requesting all pages with params: {params}")
            resp = session.get(api_url, params=params).json()
            for p in resp["query"]["allpages"]:
                logger.log("DEBUG", f"Yielding page: {p['title']}")
                yield p

            if "continue" in resp:
                apcontinue = resp["continue"]["apcontinue"]
                logger.log("DEBUG", f"Continuing all pages, next apcontinue: {apcontinue}")
            else:
                cont = False
                logger.log("DEBUG", "Finished fetching all pages")

    def get_category_pages(self, category_name):
        api_url = self.url + "api.php"
        session = self.session
        params = {
            "action": "query",
            "list": "categorymembers",
            "cmtitle": f"Category:{category_name}",
            "cmlimit": "50",
            "format": "json"
        }

        cont = True
        cmcontinue = None

        while cont:
            if cmcontinue:
                params["cmcontinue"] = cmcontinue
            logger.log("DEBUG", f"Requesting category pages for '{category_name}' with params: {params}")
            resp = session.get(api_url, params=params).json()
            for p in resp["query"]["categorymembers"]:
                logger.log("DEBUG", f"Yielding category page: {p['title']}")
                yield p

            if "continue" in resp:
                cmcontinue = resp["continue"]["cmcontinue"]
                logger.log("DEBUG", f"Continuing category pages, next cmcontinue: {cmcontinue}")
            else:
                cont = False
                logger.log("DEBUG", f"Finished fetching pages for category: {category_name}")
