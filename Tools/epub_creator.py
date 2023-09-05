"""Retrieve metadata from docx file, convert it to html, edit it and convert it to epub file"""

import os
import sys

# Convert html to epub
from jinja2 import Environment, FileSystemLoader
from pypub import Epub, create_chapter_from_html

# Get docx infos
from Tools.config import TEMPLATES

import sys





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


if __name__ == "__main__":
    print("Should NOT be executed directly")
    sys.exit(-1)
