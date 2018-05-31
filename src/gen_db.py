#!/usr/bin/python3
import sqlalchemy
import os
import re
import urllib.parse
import bs4
from bs4 import BeautifulSoup, Tag

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

docset_dir = 'build/QuantumESPRESSO.docset'
contents_dir = os.path.join(docset_dir, 'Contents')
resources_dir = os.path.join(contents_dir, 'Resources')
documents_dir = os.path.join(resources_dir, 'Documents')
sqlite_db_path = os.path.join(resources_dir, 'docSet.dsidx')

Base = declarative_base()

class SearchIndex(Base):

    __tablename__ = 'searchIndex'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    type = sqlalchemy.Column(sqlalchemy.String)
    path = sqlalchemy.Column(sqlalchemy.String)

def get_packages():
    for html_filename in os.listdir(documents_dir):
        match = re.search(r'^INPUT_(.*)\.html$', html_filename)
        if not match: continue
        package_name = match.group(1)
        yield package_name

def process_package(session, name: str):
    print(name)
    filename = 'INPUT_%s.html' % (name)
    session.add(SearchIndex(
        name=name,
        type='Package',
        path=filename
    ))
    process_input_doc(session, package_name, filename)

def process_input_doc(session, package_name: str, filename: str):
    html_path = os.path.join(documents_dir, filename)
    soup = BeautifulSoup(open(html_path), 'html.parser')
    process_sections(session, package_name, filename, soup)
    process_variables(session, package_name, filename, soup)
    add_entries(session, package_name, filename, soup)
    with open(html_path, 'w') as fp:
        fp.write(str(soup))

def generate_anchor_name(entry_type: str, entry_name: str):
    return '//apple_ref/%s/%s' % (entry_type, urllib.parse.quote(entry_name))

def add_entries(session, package_name: str, filename: str, soup):
    section_name = ''
    for anchor in soup.select('a.dashAnchor'):
        anchor_name = anchor['name']
        res = re.search(r'^//apple_ref/([^/]+)/([^/]+)$', anchor_name)
        entry_type = res.group(1)
        item_name = urllib.parse.unquote(res.group(2))
        if entry_type == 'Section':
            section_name = item_name
            entry_name = '%s.%s' % (package_name, section_name)
        else:
            entry_name = '%s.%s.%s' % (package_name, section_name, item_name)
        path = '%s#%s' % (filename, anchor_name)
        session.add(SearchIndex(
            name=entry_name,
            type=entry_type, 
            path=path
        ))

def process_sections(session, package_name: str, filename: str, soup):
    for section_span in soup.select('span.namelist'):
        section_name = section_span.contents[1]
        name = '%s.%s' % (package_name, section_name)

        anchor_name = generate_anchor_name('Section', section_name)
        anchor = Tag(name='a', builder=soup.builder, attrs={
            'name': anchor_name,
            'class': 'dashAnchor'
        })

        path = '%s#%s' % (filename, anchor_name)

        section_span.insert_before(anchor)

    for section_span in soup.select('span.card'):
        section_name = str(section_span.contents[0]).strip()
        name = '%s.%s' % (package_name, section_name)

        anchor_name = generate_anchor_name('Section', section_name)
        anchor = Tag(name='a', builder=soup.builder, attrs={
            'name': anchor_name,
            'class': 'dashAnchor'
        })

        path = '%s#%s' % (filename, anchor_name)

        section_span.insert_before(anchor)

def process_variables(session, package_name: str, filename: str, soup):
    for variable_th in soup.select('tr > th'):
        if not variable_th.has_attr('style'): continue
        if 'background: #ffff99; padding: 2 2 2 10;' not in variable_th['style']: continue
        variable_name = variable_th.contents[0]
        if type(variable_name) != bs4.element.NavigableString: continue
        variable_name = str(variable_name).strip()
        variable_name = re.sub('\s+', ' ', variable_name)
        if variable_name == '': continue
        name = '%s.%s' % (package_name, variable_name)

        anchor_name = generate_anchor_name('Variable', variable_name)
        anchor = Tag(name='a', builder=soup.builder, attrs={
            'name': anchor_name,
            'class': 'dashAnchor'
        })

        path = '%s#%s' % (filename, anchor_name)

        #session.add(SearchIndex(
            #name=name,
            #type='Variable',
            #path=path
        #))

        variable_th.insert_before(anchor)

if __name__ == '__main__':
    engine = sqlalchemy.create_engine('sqlite:///%s' % (sqlite_db_path), echo=True)
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    general_guides = [
        SearchIndex(
            name="User's Guide",
            type='Guide',
            path='user_guide/index.html'
        ),
        SearchIndex(
            name="Developers's Manual",
            type='Guide',
            path='developer_man/index.html'
        )
    ]

    package_specific_guides = [
        SearchIndex(
            name="%s User's Guide" % (item[0]),
            type='Guide',
            path='%s_user_guide/index.html' % (item[1])
        )
        for item in [
            ('PWscf', 'pw'),
            ('CP', 'cpv'),
            ('PostProc', 'pp'),
            ('PHonon', 'ph'),
            ('PWneb', 'neb')
        ]
    ]

    session.add_all(general_guides)
    session.add_all(package_specific_guides)

    for package_name in get_packages():
        process_package(session, package_name)

    session.commit()