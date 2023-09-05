"""Get docx metadata required for Epub creation and HTML parsing"""
from dataclasses import dataclass

from docx import Document
from bs4 import BeautifulSoup

from Tools.config import copyright_text


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
    rights = copyright_text(created_year, author)

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
