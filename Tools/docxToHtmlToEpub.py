"""Retrieve metadata from docx file, convert it to html, edit it and convert it to epub file"""
from dataclasses import dataclass

import os
import sys

# Convert docx to html
from pydocx import PyDocX

# Edit html
from bs4 import BeautifulSoup

# Convert html to epub
from jinja2 import Environment, FileSystemLoader
from pypub import Epub, create_chapter_from_html

# Get docx infos
from docx import Document

# Import config
# import sys
# sys.path.append( '../' )
from config import *

######### TESTING ##########
###### MOVE TO CONFIG ######
TEMPLATES = "Templates/"  #
###### MOVE TO CONFIG ######

@dataclass
class EpubInfo:
    """
    Epub Specification
    """

    title: str
    rights: str
    creator: str
    created_year: str
    subtitle: str = ""
    language: str = "en"

    def __init__(
        self, title, rights, creator, created_year, subtitle="", language="en"
    ):
        self.title = title
        self.subtitle = subtitle
        self.rights = rights
        self.creator = creator
        self.created_year = created_year
        self.language = language


def docx_to_html(docx_file, html_file):
    """Convert docx file to html file and save a prettified version as a file"""
    html = PyDocX.to_html(docx_file)
    soup = BeautifulSoup(html, "html.parser")

    # Save html string variable into a file for debugging purposes
    with open(html_file, "w", encoding="utf-8") as file:
        file.write(soup.prettify())

    return html


def parse_docx(docx_file):
    """Parse docx file and return retrieved file infos"""
    # Retrieve docx infos
    print(docx_file)
    document = Document(docx_file)
    title = document.core_properties.title
    author = document.core_properties.author
    created = document.core_properties.created
    created_year = ""
    if not isinstance(created, type(None)):
        created_year = created.year
    rights = copyrightText(created_year, author)

    return EpubInfo(
        title=title,
        rights=rights,
        creator=author,
        created_year=created_year,
        language="en",
    )


def parse_html(epub_data, html):
    """Parse html file and return remaining EpubInfo data and the BeautifulSoup html"""
    soup = BeautifulSoup(html, "html.parser")

    if not bool(epub_data.title) and soup.h1:
        epub_data.title = soup.h1.text
    elif not bool(epub_data.title) and soup.h1 is None:
        print("[WARNING] No title found in docx file")

    if not bool(epub_data.subtitle) and soup.h3:
        epub_data.subtitle = soup.h3.text

    return (
        EpubInfo(
            epub_data.title,
            epub_data.rights,
            epub_data.creator,
            epub_data.created_year,
            epub_data.subtitle,
            epub_data.language,
        ),
        soup,
    )


def create_epub(output_file, epub, soup):
    """Create epub file from EpubInfo and BeautifulSoup html"""
    book = Epub(
        epub.title,
        creator=epub.creator,
        subtitle=epub.subtitle,
        language="en",
        rights=epub.rights,
        css_paths=["Styles/styles.css"],
    )

    # If output_file already exists, delete it (=overwrite)
    if os.path.exists(output_file):
        os.remove(output_file)
        print("Previous epub file removed")

    jinja_env = Environment(loader=FileSystemLoader(TEMPLATES))

    book.builder.template = jinja_env.get_template("coverpage.xhtml.j2")
    with book.builder as builder:
        builder.begin()
        builder.template = jinja_env.get_template("page.xhtml.j2")
        headers_list = soup.find_all("h2")

        for header in headers_list:
            chapter_text = ""
            print(f"Adding chapter {headers_list.index(header)+1}/{len(headers_list)}")
            while header.next_sibling is not None and header.next_sibling.name != "h2":
                chapter_text += str(header.next_sibling)
                header.next_sibling.extract()

            chapter = create_chapter_from_html(chapter_text.encode(), header.text)
            assign = book.assign_chapter()
            book.builder.render_chapter(assign, chapter)
        builder.finalize(output_file)


def test():
    """Testing function, use all functions from this file"""
    file = "Test - Formatted"
    docx_file = file + ".docx"
    html_file = file + ".html"
    epub_file = file + ".epub"
    epub_data = parse_docx(docx_file)
    epub_data, soup = parse_html(epub_data, docx_to_html(docx_file, html_file))

    create_epub(epub_file, epub_data, soup)


if __name__ == "__main__":
    # test()
    print("Should NOT be executed directly")
    sys.exit(-1)
