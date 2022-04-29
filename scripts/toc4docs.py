import re
from pathlib import Path
from bs4 import BeautifulSoup
from lxml.html import fromstring
from tqdm.cli import tqdm

DOCSET_ROOT = 'qe.docset'
DOCSET_DOCS = Path(f'{DOCSET_ROOT}/Contents/Resources/Documents')

def insert_anchor(soup: BeautifulSoup, name: str, type: str, id: str):
    id = id.lstrip("#")
    tag = soup.find(None, {"name": id.lstrip("#")})
    anchor = BeautifulSoup(f"<a name='//apple_ref/cpp/{type}/{name}' class='dashAnchor' />", features="lxml")
    tag.insert_after(anchor)

if __name__ == "__main__":

    # Input descriptions

    for file in tqdm(DOCSET_DOCS.glob("Doc/INPUT_*.html")):

        path = file.relative_to(DOCSET_DOCS)
        soup = BeautifulSoup(open(file), features="lxml")

        for a in soup.select("td > blockquote blockquote > p > a"):
            try:
                title = a.text.lstrip("&").rstrip(":").strip()
                if title == title.upper():
                    insert_anchor(soup, title, "Section", a["href"])
            except KeyError:
                pass

        for a in soup.select("td > blockquote > blockquote blockquote > a"):
            try:
                insert_anchor(soup, a.text, "Parameter", a["href"])
            except KeyError:
                pass
    
        with open(file, "w") as fp:
            fp.write(str(soup))
