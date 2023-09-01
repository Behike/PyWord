from dataclasses import dataclass
# Get docx infos
import os
from docx import Document
# Convert docx to html
from pydocx import PyDocX
# Edit html
from bs4 import BeautifulSoup
# Convert html to epub
from pypub import Epub, create_chapter_from_html
from jinja2 import Environment, FileSystemLoader

# Import config
import sys
sys.path.append( '../' )
from config import *

######### TESTING ##########
###### MOVE TO CONFIG ######
TEMPLATES = "Templates/"   #
                           #
file = "Test - Formatted"  #
docx_file = file + '.docx' #
html_file = file + '.html' #
epub_file = file + '.epub' #
###### MOVE TO CONFIG ######

############### MOVE ELSEWHERE? ###############
@dataclass
class EpubInfo:
    """
    Epub Specification
    """
    title:        str
    rights:       str
    creator:      str
    created_year: str
    subtitle:     str = ''
    language:     str = 'en'

    def __init__(self, title, rights, creator, created_year, subtitle = '', language='en'):
        self.title         = title
        self.subtitle      = subtitle
        self.rights        = rights
        self.creator       = creator
        self.created_year  = created_year
        self.language      = language
############### MOVE ELSEWHERE? ###############


def docxToHtml(docx_file):
    return PyDocX.to_html(docx_file)

def parseDocx(docx_file):
    # Retrieve docx infos
    document = Document(docx_file)
    title = document.core_properties.title
    author = document.core_properties.author
    created = document.core_properties.created
    created_year = "" if type(created) == type(None) else created.year
    rights = copyrightText(created_year, author)
    
    return EpubInfo(title=title, rights=rights, creator=author, created_year=created_year, language='en')

def parseHtml(html):
    html = docxToHtml(docx_file)

    soup = BeautifulSoup(html, 'html.parser')

    title, rights, creator, created_year, language = parseDocx(docx_file)
    if (not bool(title)):
        title = soup.h1.text
    if (not bool(subtitle)):
        subtitle = soup.h3.text

    # Save html string variable into a file for debugging purposes
    with open(html_file, 'w', encoding="utf-8") as f:
        f.write(soup.prettify())
        
    return EpubInfo(title, rights, creator, created_year, subtitle, language), soup

def createEpub(epub, soup):
    # Create the epub object
    book = Epub(epub.title, creator=epub.author, subtitle=epub.subtitle, language='en', rights=epub.rights, css_paths=['styles.css'])

    # If epub_file already exists, delete it (=overwrite)
    if os.path.exists(epub_file):
        os.remove(epub_file)
        print('Previous epub file removed')
        
    jinja_env = Environment(loader=FileSystemLoader(TEMPLATES))

    book.builder.template = jinja_env.get_template('coverpage.xhtml.j2')
    with book.builder as builder:
        dirs = builder.begin()
        builder.template = jinja_env.get_template('page.xhtml.j2')
        headers_list = soup.find_all('h2')

        for header in headers_list:
            chapter_text = ''
            while header.next_sibling != None and header.next_sibling.name != 'h2':
                print(f'Adding chapter {headers_list.index(header)+1}/{len(headers_list)}')
                chapter_text += str(header.next_sibling)
                header.next_sibling.extract()
                
            chapter = create_chapter_from_html(chapter_text.encode(), header.text)
            assign = book.assign_chapter()
            book.builder.render_chapter(assign, chapter)
        builder.finalize(epub_file)


def main():
    epubData, soup = parseHtml(docxToHtml(docx_file))
    createEpub(epubData, soup)

if __name__ == '__main__':
    main()
    exit(0)
# if __name__ == '__main__':
#     print('Should NOT be executed directly')
#     exit(-1)