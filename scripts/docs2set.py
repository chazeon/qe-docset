import re, sqlite3
from pathlib import Path
from bs4 import BeautifulSoup
from typing import Optional
from urllib.parse import urljoin

DOCSET_ROOT = 'qe.docset'
DOCSET_DOCS = Path(f'{DOCSET_ROOT}/Contents/Resources/Documents')

class Docset():

    def __init__(self) -> None:
        self.conn = sqlite3.connect(f'{DOCSET_ROOT}/Contents/Resources/docSet.dsidx')
        self.cur = self.conn.cursor()

        try:
            self.cur.execute('DROP TABLE searchIndex;')
        except:
            pass

        self.cur.execute('CREATE TABLE searchIndex(id INTEGER PRIMARY KEY, name TEXT, type TEXT, path TEXT);')
        self.cur.execute('CREATE UNIQUE INDEX anchor ON searchIndex (name, type, path);')
    
    def __del__(self):
        self.conn.commit()
        self.conn.close()

    def insert_index(self, name, type, path):
        self.cur.execute('INSERT OR IGNORE INTO searchIndex(name, type, path) VALUES (?,?,?)', (name, type, path))

    def find_by_name(self, name) -> list:
        self.cur.execute('SELECT * FROM searchIndex WHERE (name = ?)', (name,))
        return self.cur.fetchall()

    def find_by_path(self, path) -> list:
        self.cur.execute('SELECT * FROM searchIndex WHERE (path = ?)', (path,))
        return self.cur.fetchall()

def get_page_title(soup) -> Optional[str]:
    title = soup.find("title")
    return title.text
    
if __name__ == "__main__":

    docset = Docset()

    # Website pages

    for file in DOCSET_DOCS.glob("**/*.html"):

        if str(file).startswith(str(DOCSET_DOCS / "Doc")): continue

        path = file.relative_to(DOCSET_DOCS)
        soup = BeautifulSoup(open(file), features="lxml")

        title = soup.find("h1").text
        docset.insert_index(title.capitalize(), "Resource", str(path))

    # Input descriptions

    for file in DOCSET_DOCS.glob("Doc/INPUT_*.html"):

        path = file.relative_to(DOCSET_DOCS)
        soup = BeautifulSoup(open(file), features="lxml")

        title = get_page_title(soup)
        command = re.match(r"^(\S+): input description", title).group(1)
        docset.insert_index(command, "Command", str(path))

        for a in soup.select("td > blockquote blockquote > p > a"):
            try:
                title = a.text.lstrip("&").rstrip(":").strip()
                if title == title.upper():
                    docset.insert_index(title, "Section", urljoin(str(path), a["href"]))
            except KeyError:
                pass

        for a in soup.select("td > blockquote > blockquote blockquote > a"):
            try:
                docset.insert_index(a.text, "Parameter", urljoin(str(path), a["href"]))
            except KeyError:
                pass

       
    # Guides

    for file in DOCSET_DOCS.glob("Doc/*_guide/index.html"):

        path = file.relative_to(DOCSET_DOCS)
        soup = BeautifulSoup(open(file), features="lxml")

        title = get_page_title(soup)
        docset.insert_index(title, "Guide", str(path))

        for a in soup.select("ul > li > a"):
            title = re.sub(r'^[\d\.]+ ', '', a.text)
            title = re.sub(r'\n', '', title)
            print(title)
            docset.insert_index(title, "Entry", urljoin(str(path), a["href"]))
            