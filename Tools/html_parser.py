"""This module contains functions for parsing and editing html files"""
# Convert docx to html
from pydocx import PyDocX

# Work with html
from bs4 import BeautifulSoup

from Tools.metadata_parser import parse_docx, parse_html, EpubInfo

# HTML equivalent of Word/Human styles
# Subtitle corresponds to the line below the main title
HEADERS_HTML = {
    "Title": "h1",
    "Chapter": "h2",
    "Subtitle": "h3",
    "Copyrights": "h4",
    "Normal": "p",
}

# HTML equivalent of Word/Human font styles
FONTS_HTML = {
    "Bold": "strong",
    "Italic": "i",
    "Underline": "u",
    "Strike": "s",
}


def docx_to_html(docx_file, html_file):
    """Convert docx file to html file and save a prettified version as a file (for debugging)"""
    html = PyDocX.to_html(docx_file)
    soup = BeautifulSoup(html, "html.parser")

    # Save html string variable into a file for debugging purposes
    with open(html_file, "w", encoding="utf-8") as file:
        file.write(soup.prettify())

    return html

def iterate_html(metadata: EpubInfo, html):
    """Iterate through html and yield each element"""
    soup = BeautifulSoup(html, "html.parser")
    body_tag = soup.body

    for child in body_tag.children:
        if (child.get_text().trim() == metadata.title.trim()):
            print(child.get_text())



    h1_list = soup.find_all("h1")
    print(h1_list)
    h2_list = soup.find_all("h2")
    print(h2_list)
    h3_list = soup.find_all("h3")
    print(h3_list)
    h4_list = soup.find_all("h4")
    print(h4_list)

    # for element in soup:
        # yield element

    # 1] We have specific styles for chapters

    # 2] We already have the titles/copyrights written at the very beginning
    # 3] We have HEADER_1_NAMES_LIST to recognize chapters
    # 4] We have numbers to recognize chapters
    # 5] ? We have the length of the text to recognize chapters ?


if __name__ == "__main__":
    file = "Test"
    docx_file = file + ".docx"
    html_file = file + ".html"
    epub_file = file + ".epub"
    html = docx_to_html(docx_file, html_file)
    epub_data = parse_docx(docx_file)
    epub_data = parse_html(epub_data, html)
    iterate_html(epub_data, html)