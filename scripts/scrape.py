import re
from pathlib import Path
import urllib.parse
from os import makedirs
from functools import lru_cache

import requests
import requests_cache
from bs4 import BeautifulSoup



DOCSET_ROOT = Path('qe.docset')
DOCSET_DOCS = DOCSET_ROOT / 'Contents/Resources/Documents'

class Scraper():

    '''MediaWiki API'''

    CACHE = 'cache'


    def __init__(self) -> None:
        self.session = requests_cache.CachedSession(self.CACHE)
        self.docs = []

    @staticmethod
    def get_url_path(url: str) -> str:
        path = urllib.parse.urlparse(url).path
        return path if not path.endswith("/") else f"{path}/index.html"

    @staticmethod
    def clean_url(url: str) -> str:
        'Remove the element IDs from URLs.'
        parsed = urllib.parse.urlparse(url)
        parsed = parsed._replace(fragment='')
        return urllib.parse.urlunparse(parsed)
    
    @staticmethod
    def clean_html(soup: BeautifulSoup, url: str) -> BeautifulSoup:
        rel = (len(Path(urllib.parse.urlsplit(url).path).parts) - 1) * '../'
        for a in soup.find_all('a'):
            try:
                a["href"] = re.sub(r"^/Doc/(.*)/$", rel + r"Doc/\1/index.html", a["href"])
                a["href"] = re.sub(r"^/Doc/", rel + r"Doc/", a["href"])
                a["href"] = re.sub(r"^https://www.quantum-espresso.org/(.*)/$", rel + r"\1/index.html", a["href"])
            except KeyError:
                continue
        return soup
    
    @staticmethod
    def find_docs(soup: BeautifulSoup):
        for a in soup.find_all('a'):
            try:
                if a["href"].startswith("/Doc"):
                    yield "https://www.quantum-espresso.org" + a["href"]
            except:
                pass

    def scrape_website_page(self, url) -> str:
        path = DOCSET_DOCS / self.get_url_path(url)[1:]
        if not path.parent.exists():
            makedirs(path.parent)
        response = self.session.get(url)
        soup = BeautifulSoup(response.text, features="lxml")
        self.docs.extend(self.find_docs(soup))
        with open(path, "w") as fp:
            self.clean_html(soup, url)
            fp.write(str(soup.select_one("#primary")))
        return str(soup)
    
    @lru_cache
    def scrape_doc(self, url) -> str:
        path = DOCSET_DOCS / self.get_url_path(url)[1:]
        if not path.parent.exists():
            makedirs(path.parent)
        response = self.session.get(url)
        with open(path, "wb") as fp:
            fp.write(response.content)
        return response.text
    
    def scrape_full_doc(self, root) -> str:
        content = self.scrape_doc(root)
        soup = BeautifulSoup(content, features="lxml")
        for a in soup.find_all('a'):
            try:
                url = urllib.parse.urljoin(root, a['href'])
                url = self.clean_url(url)
                self.scrape_doc(url)
            except KeyError:
                continue
        for img in soup.find_all('img'):
            url = urllib.parse.urljoin(root, img['src'])
            self.scrape_doc(url)


if __name__ == "__main__":

    scraper = Scraper()

    # scraper.get_website_

    scraper.scrape_website_page('https://www.quantum-espresso.org/documentation/')
    scraper.scrape_website_page('https://www.quantum-espresso.org/other-resources/')
    scraper.scrape_website_page('https://www.quantum-espresso.org/pseudopotentials/')
    scraper.scrape_website_page('https://www.quantum-espresso.org/auxiliary-software/')
    scraper.scrape_website_page('https://www.quantum-espresso.org/documentation/input-data-description/')
    scraper.scrape_website_page('https://www.quantum-espresso.org/documentation/package-specific-documentation/')

    for docurl in scraper.docs:
        if docurl.endswith(".html"):
            scraper.scrape_doc(docurl)
        else:
            scraper.scrape_full_doc(docurl)

