"""Get docx metadata required for Epub creation and HTML parsing"""
import sys
import logging

from dataclasses import dataclass
from bs4 import BeautifulSoup
from Config.config import copyright_text, SUBTITLE_MAX_SEARCH
from docx import Document

logger = logging.getLogger(__name__)


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
        logger.info("[WARNING] No title found in docx file")

    # If no subtitle is found, use the h3 tag if there is only one at the beginning of the document
    if not bool(epub_data.subtitle) and len(soup.body.find_all("h3")) == 1 and str(soup.body).find(str(soup.h3)) and str(soup.body).find(str(soup.h3)) < SUBTITLE_MAX_SEARCH:
        epub_data.subtitle = soup.h3.text

    return epub_data


if __name__ == "__main__":
    logger.info("Nothing to do")
    sys.exit(0)
