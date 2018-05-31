import jinja2
import requests
import bs4
import urllib.parse
import os

url_base = 'https://www.quantum-espresso.org/resources/users-manual'

def scrap_content(rel_path: str):
    res = requests.get(urllib.parse.urljoin(url_base, rel_path))
    soup = bs4.BeautifulSoup(res.text, 'html.parser')
    for anchor in soup.select('a'):
        if not anchor.has_attr('href'): continue
        if anchor['href'].startswith('/Doc/'):
            anchor['href'] = anchor['href'][5:]
            if anchor['href'].endswith('user_guide'):
                anchor['href'] = anchor['href'] + '/index.html'
    return soup.select('div.maincontent')[0]

if __name__ == '__main__':
    with open('res/index_template.html', encoding='utf8') as fp:
        template = jinja2.Template(fp.read())
    rendered = template.render(
        general_document_info=scrap_content('users-manual'),
        input_data_descriptions_info=scrap_content('users-manual/input-data-description'),
        package_specific_documents_info=scrap_content('users-manual/specific-documentation')
    )
    with open(os.path.join(
        'build',
        'QuantumESPRESSO.docset',
        'Contents',
        'Resources',
        'Documents',
        'index.html'
    ), 'w', encoding='utf8') as fp:
        fp.write(rendered)