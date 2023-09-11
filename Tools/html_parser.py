"""This module contains functions for parsing and editing html files"""
# Convert docx to html
from collections import Counter
from re import IGNORECASE, match, search, escape, compile
from pydocx import PyDocX

# Work with html
from bs4 import BeautifulSoup
from epub_creator import create_epub
from config import CAPITALIZE_WORDS_LIST, CHAPTER_MAX_LENGTH, HEADER_1_NAMES_LIST, NUMBER_DICT, NOT_HEADER_WORDS, DEBUG_LEVEL

from metadata_parser import parse_docx, parse_html, EpubInfo

import sys

# HTML equivalent of Word/Human styles
# Subtitle corresponds to the line below the main title
HEADERS_TO_HTML = {
    "Title": "h1",
    "Chapter": "h2",
    "Subtitle": "h3",
    "Copyrights": "h4",
    "Normal": "p",
}

# Word equivalent of HTML tags we want in our case
HTML_TO_HEADERS = {
    "h1": "Title",
    "h2": "Chapter",
    "h3": "Subtitle",
    "h4": "Copyrights",
    "p": "Normal",
}

# Word equivalent of HTML tags (for logging purposes)
HTML_TO_WORD_HEADERS = {
    "title": "Title",
    "h1": "Heading 1",
    "h2": "Heading 2",
    "h3": "Heading 3",
    "h4": "Heading 4",
    "p": "Normal",
}

# HTML equivalent of Word/Human font styles
FONTS_HTML = {
    "Bold": "strong",
    "Italic": "i",
    "Underline": "u",
    "Strike": "s",
}

list_of_actions_logs = ""
chapter_number = 1

def capitalizeSentences(text):
    """Capitalize sentences in text except for CAPITALIZE_WORDS_LIST words"""
    text_list = text.split()
    for i in range(len(text_list)):
        text_list[i] = text_list[i].lower()
        if (not text_list[i] in CAPITALIZE_WORDS_LIST or i == 0):
            text_list[i] = text_list[i].capitalize()

    text = ' '.join(text_list)
    return text


def chapter_finder(text):
    """Test if text is (or can be) a chapter and format it"""
    is_chapter = False
    not_header_words_present = [ele for ele in NOT_HEADER_WORDS if search(r"(?i)(?<!\S)" + escape(ele) + r"[\.:]{0,1}" + r"(?!\S)", text)]   
    
    # If the paragraph is at most CHAPTER_MAX_LENGTH characters long and starts with one of the header_1_names_list words
    if ((len(text) <= CHAPTER_MAX_LENGTH) and (not not_header_words_present) and text[-1] != '.'):
        ## Find elements in paragraph text
        # List of header 1 keywords present at the beginning of the text (empty or one word only)
        header_1_keyword_first = [ele for ele in HEADER_1_NAMES_LIST if text.upper().startswith(ele)]
        
        # Search for chapter number
        if (header_1_keyword_first and len(text.split()) >= 2):
            # List of letter numbers (whole word only with eventually . or : at the end) | (?i) = case insensitive search
            letter_number = [ele for ele in NUMBER_DICT.keys() if search(r"(?i)(?<!\S)" + escape(ele) + r"[\.:]{0,1}" + r"(?!\S)", text.split()[1])]
            # List of first digits in text (with . and : characters stuck to it)
            digit = [ele for ele in text if match(r"(?<!\S)" + r"\d+" + r"[\.:]{0,1}" + r"(?!\S)", text.split()[1])]
        else:
            # List of letter numbers (whole word only with eventually . or : at the end) | (?i) = case insensitive search
            letter_number = [ele for ele in NUMBER_DICT.keys() if search(r"(?i)(?<!\S)" + escape(ele) + r"[\.:]{0,1}" + r"(?!\S)", text.split()[0])]
            # List of first digits in text (with . and : characters stuck to it)
            digit = [ele for ele in text if match(r"(?<!\S)" + r"\d+" + r"[\.:]{0,1}" + r"(?!\S)", text.split()[0])]

        # If there is a chapter number and no header keyword
        if ((not header_1_keyword_first) and (letter_number or digit) and len(text.split()) > 1):
            is_chapter = True

        # If there is a header keyword, a chapter number and a chapter name
        elif (header_1_keyword_first and (letter_number or digit) and len(text.split()) > 2):
            is_chapter = True

        # If whole text is a number (digit)
        if (digit and text == digit):
            is_chapter = True

        # If whole text is a number (in letter) convert it to number
        elif (letter_number and text.upper() == letter_number[0]):
            is_chapter = True

        if (is_chapter):
            print(f"Found a chapter: {text}")
            text = capitalizeSentences(text)
    return is_chapter


def chapter_formatter(text, chapter_number):
    global list_of_actions_logs
    """Format text as a chapter"""
    
    old_text = text


    # List of header 1 keywords present at the beginning of the text (empty or one word only)
    header_1_keyword_first = [ele for ele in HEADER_1_NAMES_LIST if text.upper().startswith(ele)]
    
    # Search for chapter number
    if (header_1_keyword_first and len(text.split()) >= 2):
        # List of letter numbers (whole word only with eventually . or : at the end) | (?i) = case insensitive search
        letter_number = [ele for ele in NUMBER_DICT.keys() if search(r"(?i)(?<!\S)" + escape(ele) + r"[\.:]{0,1}" + r"(?!\S)", text.split()[1])]
        # List of first digits in text (with . and : characters stuck to it)
        digit = [ele for ele in text if match(r"(?<!\S)" + r"\d+" + r"[\.:]{0,1}" + r"(?!\S)", text.split()[1])]
    else:
        # List of letter numbers (whole word only with eventually . or : at the end) | (?i) = case insensitive search
        letter_number = [ele for ele in NUMBER_DICT.keys() if search(r"(?i)(?<!\S)" + escape(ele) + r"[\.:]{0,1}" + r"(?!\S)", text.split()[0])]
        # List of first digits in text (with . and : characters stuck to it)
        digit = [ele for ele in text if match(r"(?<!\S)" + r"\d+" + r"[\.:]{0,1}" + r"(?!\S)", text.split()[0])]

    # If there is a chapter number and no header keyword
    if ((not header_1_keyword_first) and (letter_number or digit) and len(text.split()) > 1):
        # Add "Chapter" at the beginning of the text
        text = HEADER_1_NAMES_LIST[0].capitalize() + " " + text
        header_1_keyword_first, digit, letter_number = [], [], []
        list_of_actions_logs = list_of_actions_logs + " [No header keyword + number]"
    # If there is a header keyword, a chapter number and a chapter name
    elif (header_1_keyword_first and (letter_number or digit) and len(text.split()) > 2):
        header_1_keyword_first, digit, letter_number = [], [], []
        list_of_actions_logs = list_of_actions_logs + " [Header keyword + number]"

    # If whole text is a number (digit)
    if (digit and text == digit):
        text = HEADER_1_NAMES_LIST[0].capitalize() + " " + text
        list_of_actions_logs = list_of_actions_logs + " [Whole Text = Number]"

    # If whole text is a number (in letter) convert it to number
    elif (letter_number and text.upper() == letter_number[0]):
        text = HEADER_1_NAMES_LIST[0].capitalize() + " " + str(NUMBER_DICT[letter_number[0]])
        list_of_actions_logs = list_of_actions_logs + " [Text = Letter number]"

    # Replace chapter name number in letter with the corresponding number
    if (letter_number):
        chapter_number_found = ''
        for substring in NUMBER_DICT.keys():
            if substring in text.upper():
                chapter_number_found = substring
        if (chapter_number_found != ''):
            pattern = compile(chapter_number_found, IGNORECASE)
            text = pattern.sub(str(NUMBER_DICT[chapter_number_found.upper()]), text)
    list_of_actions_logs = list_of_actions_logs + " [Letter to number]"
    text = text.replace('.', ' ')     # Replace . with single space
    text = text.replace(':', ' ')     # replace : with single space
    _RE_COMBINE_WHITESPACE = compile(r"\s+")
    text = _RE_COMBINE_WHITESPACE.sub(" ", text).strip() # Replace multiple spaces with only one space


    if (header_1_keyword_first):
        # logging.debug("Header 1 correct: " + text)
        print("Header 1 correct: " + text)
        clean_counter = clean_counter + 1
    else:
        text = HEADER_1_NAMES_LIST[0].capitalize() + " " + str(chapter_number) + " - " + text
        chapter_number = chapter_number + 1
        # logging.debug("[UPDATED] " + old_text + " --> " + text)
        print("[UPDATED] " + old_text + " --> " + text)
    print(list_of_actions_logs)
    text = capitalizeSentences(text)
    return text

def docx_to_html(docx_file, html_file):
    """Convert docx file to html file and save a prettified version as a file (for debugging)"""
    html = PyDocX.to_html(docx_file)
    soup = BeautifulSoup(html, "html.parser")

    # Save html string variable into a file for debugging purposes
    with open(html_file, "w", encoding="utf-8") as file:
        file.write(soup.prettify())

    return html

def iterate_html(metadata: EpubInfo, html):
    global list_of_actions_logs
    """Iterate through html and yield each element"""
    soup = BeautifulSoup(html, "html.parser")
    body_tag = soup.body

    word_count = 0
    most_common_tag = ''
    reg_headers = compile("h[1-6]*")
    list_of_found_headers = body_tag.find_all(reg_headers)
    if (len(list_of_found_headers) > 1):
        list_of_tags = []
        for tag in body_tag.find_all(reg_headers):
            list_of_tags.append(tag.name)

        most_common_tag = max(list_of_tags, key=Counter(list_of_tags).get)
        print(f"Found multiple '{HTML_TO_WORD_HEADERS[most_common_tag]}', using them as chapters")
        
    child_count = 0
    chapter_number = 1
        
    for child in body_tag.children:
        list_of_actions_logs = ""

        old_child = child

        # Remove empty paragraphs
        if (child.get_text().strip() == ""):
            print(f"Empty paragraph skipped")
            # print(child.extract())
            continue

        # If title is found in the first 3 paragraphs, remove it (as it will be properly added later)
        if (child_count < 3 and child.get_text().strip() == metadata.title.strip()):
            print(f"Found title: '{child.string.extract()}', removing it")
            continue
        elif (child_count >= 3 and child.get_text().strip() == metadata.title.strip()):
            print(f"/!\ Found title: '{child.string.extract()}' but NOT removing it as it's not in the first {child_count} paragraphs")

        if (most_common_tag != '' and child.name and
            child.name == most_common_tag):
                if (child.string is not None):
                    child.string = child.get_text().strip()
                print(f"[{child.name} > {HEADERS_TO_HTML['Chapter']}] Set '{child}' as a chapter")
                child.string = child.get_text()
                child.name = HEADERS_TO_HTML["Chapter"]
        elif (most_common_tag != '' and child.name and match(reg_headers, child.name) and
              (int(child.name[1]) < int(most_common_tag[1]))):
            print(f"Found uncommon header '{child.name}', ignored")

        # Find chapter in text if required and format chapter
        if (child.name == HEADERS_TO_HTML["Chapter"] or (chapter_finder(child.get_text().strip()) and most_common_tag != '')):
            child.string = chapter_formatter(child.get_text().strip(), chapter_number)
            chapter_number += 1
            child.name = HEADERS_TO_HTML["Chapter"]

        # Count number of childs
        child_count += 1

        # Count number of words in child.get_text()
        word_count += len(child.get_text().split())

        if (old_child != child):
            print(f"{list_of_actions_logs} {old_child} --> {child}")
            # logging.debug("%s \"%s\" --> \"%s\"", list_of_actions_logs, old_child, child)

    print(f"Found {child_count} paragraphs and {word_count} words")
        
    # for element in soup:
        # yield element

    # 1] We have specific styles for chapters
    # 2] We already have the titles/copyrights written at the very beginning
    # 3] We have HEADER_1_NAMES_LIST to recognize chapters
    # 4] We have numbers to recognize chapters
    # 5] ? We have the length of the text to recognize chapters ?
    # 6] If first X chapters have a header keyword/number, use this detection scheme for the remaining of the document
    # 7] Remove table, table of content and other unused stuffs and warn the user

    # FOR DEBUGGING
    with open("Output.html", "w", encoding="utf-8") as file:
        file.write(soup.prettify())
    # FOR DEBUGGING

    return soup


if __name__ == "__main__":
    file = "Test"
    # file = "A Mother's Joy"
    # file = "CHEATERS-NOT-SINNERS"
    docx_file = file + ".docx"
    html_file = file + ".html"
    epub_file = file + ".epub"
    html = docx_to_html(docx_file, html_file)
    epub_data = parse_docx(docx_file)
    epub_data = parse_html(epub_data, html)
    new_soup = iterate_html(epub_data, html)
    create_epub(epub_file, epub_data, new_soup)
