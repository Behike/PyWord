"""This module contains functions for parsing and editing html files"""
import sys
import logging

# Convert docx to html
from collections import Counter
from re import IGNORECASE, MULTILINE, findall, match, search, escape, sub
from pydocx import PyDocX

# Work with html
from bs4 import BeautifulSoup
from config import CAPITALIZE_WORDS_LIST, CHAPTER_MAX_LENGTH, HEADER_1_NAMES_LIST, NUMBER_DICT, NOT_HEADER_WORDS, MAX_MISSING_CHAPTERS

from metadata_parser import EpubInfo

logger = logging.getLogger(__name__)

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

LIST_OF_ACTIONS_LOGS = ""
chapter_number = 1

def capitalize_sentences(text):
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

        if is_chapter:
            logger.info("Found a chapter: %s", text)
    return is_chapter


def chapter_formatter(text, chapter_number):
    """Format text as a chapter"""
    global LIST_OF_ACTIONS_LOGS

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
        LIST_OF_ACTIONS_LOGS = LIST_OF_ACTIONS_LOGS + " [No header keyword + number]"
    # If there is a header keyword, a chapter number and a chapter name
    elif (header_1_keyword_first and (letter_number or digit) and len(text.split()) > 2):
        digit, letter_number = [], []
        LIST_OF_ACTIONS_LOGS = LIST_OF_ACTIONS_LOGS + " [Header keyword + number]"

    # If whole text is a number (digit)
    if (digit and text == digit):
        text = HEADER_1_NAMES_LIST[0].capitalize() + " " + text
        LIST_OF_ACTIONS_LOGS = LIST_OF_ACTIONS_LOGS + " [Whole Text = Number]"

    # If whole text is a number (in letter) convert it to number
    elif (letter_number and text.upper() == letter_number[0]):
        text = HEADER_1_NAMES_LIST[0].capitalize() + " " + str(NUMBER_DICT[letter_number[0]])
        LIST_OF_ACTIONS_LOGS = LIST_OF_ACTIONS_LOGS + " [Text = Letter number]"

    # Replace chapter name number in letter with the corresponding number
    if letter_number:
        chapter_number_found = ''
        for substring in NUMBER_DICT.keys():
            if substring in text.upper():
                chapter_number_found = substring
        if chapter_number_found != '':
            text = sub(chapter_number_found, str(NUMBER_DICT[chapter_number_found.upper()]), text, flags=IGNORECASE)
        LIST_OF_ACTIONS_LOGS = LIST_OF_ACTIONS_LOGS + " [Letter to number]"

    text = text.replace('.', ' ')     # Replace . with single space
    text = text.replace(':', ' ')     # replace : with single space
    text = sub(r"\s+", " ", text).strip() # Replace multiple spaces with only one space


    if header_1_keyword_first:
        # logging.debug("Header 1 correct: " + text)
        logger.info("Header 1 correct: %s", text)
    else:
        text = HEADER_1_NAMES_LIST[0].capitalize() + " " + str(chapter_number) + " - " + text
        chapter_number = chapter_number + 1
        # logging.debug("[UPDATED] " + old_text + " --> " + text)
        # logger.info("[UPDATED] " + old_text + " --> " + text)

    # logger.info(list_of_actions_logs)
    text = capitalize_sentences(text)
    return text

def docx_to_html(docx_file):
    """Convert docx file to html file and save a prettified version as a file (for debugging)"""
    html_output = PyDocX.to_html(docx_file)

    # Save html string variable into a file for debugging purposes
    soup = BeautifulSoup(html_output, "html.parser")
    with open(f"{docx_file}.html", "w", encoding="utf-8") as file:
        file.write(soup.prettify())

    return html_output

def iterate_html(metadata: EpubInfo, html):
    """Iterate through html and yield each element"""
    global LIST_OF_ACTIONS_LOGS

    soup = BeautifulSoup(html, "html.parser")
    body_tag = soup.body

    word_count = 0
    most_common_tag = ''
    reg_headers = r"h[1-6]"
    list_of_found_headers = body_tag.find_all(reg_headers)
    if len(list_of_found_headers) > 1:
        list_of_tags = []
        for tag in body_tag.find_all(reg_headers):
            list_of_tags.append(tag.name)

        most_common_tag = max(list_of_tags, key=Counter(list_of_tags).get)
        logger.debug("Found multiple '%s', using them as chapters", HTML_TO_WORD_HEADERS[most_common_tag])

    child_count = 0
    chapter_number = 1

    logger.info("------------------------ First analysis ------------------------")

    # Match a HEADER_1_NAMES_LIST word with punctuation and a number for Chapter keyword
    # Tag + Chapter keyword + punctuation/space (0+) + digit (1+) + punctuation/space (0+) + anything (0+) + End tag
    chapter_keywords = '|'.join(HEADER_1_NAMES_LIST)
    chapter_int_regex = fr"((<(\w+)>)\s*({chapter_keywords})([ ]*[^\w\s]*[ ]*)(\d+)([ ]*[.-:\]]*[ ]*)([^.]*?)(<\/\3>))"
    # Tag + Chapter + punctuation/space (0+) + text (1+) + punctuation/space (0+) + anything (0+) + End tag
    chapter_letter_regex = fr"((<(\w+)>)\s*({chapter_keywords})([ ]*[^\w\s]*[ ]*)([a-zA-Z]+)([ ]*[.-:\]]*[ ]*)([^.]*?)(<\/\3>))"

    chapter_int_match = findall(chapter_int_regex, str(soup), flags=MULTILINE|IGNORECASE)
    chapter_letter_match = findall(chapter_letter_regex, str(soup), flags=MULTILINE|IGNORECASE)
    str_soup = str(soup)

    missing_chapter = 0
    if chapter_int_match:
        count = 1
        for chapter_match in chapter_int_match:
            if chapter_match[5] != str(count):
                logger.info("[WARNING] Chapter %s could not be found", count)
                missing_chapter += 1
            else:
                count += 1

        if missing_chapter <= MAX_MISSING_CHAPTERS:
            for chapter_match in chapter_int_match:
                h1_html_tag_a = f"<{HEADERS_TO_HTML['Chapter']}>"
                h1_html_tag_b = f"</{HEADERS_TO_HTML['Chapter']}>"
                new_text = h1_html_tag_a + chapter_match[3] + ". " + chapter_match[5] + h1_html_tag_b
                if chapter_match[7] != '':
                    new_text = h1_html_tag_a + chapter_match[3] + ". " + chapter_match[5] + " - " + chapter_match[7] + h1_html_tag_b

                logger.info(chapter_match)
                old_text = sub(r"\s+", " ", chapter_match[0]).strip() # Replace multiple spaces with only one space
                logger.info("%s --> %s", old_text, new_text)
                str_soup = str_soup.replace(chapter_match[0], new_text)

                # int(chapter_match[5])
                # if (int(chapter_match[5]) != int(chapter_match[5])+1):
            most_common_tag = HEADERS_TO_HTML["Chapter"]
        else:
            logger.info("More than %s chapters are missing (%s), skipping this file", MAX_MISSING_CHAPTERS, missing_chapter)

    elif chapter_letter_match:
        ###### TO ADAPT ######
        # for chapter_match in CHAPTER_INT_MATCH:
        #     if (chapter_match[5] != str(count)):
        #         logger.info(f"[WARNING] Chapter {count} could not be found")
        #         missing_chapter += 1
        #     else:
        #         count += 1

        if missing_chapter <= MAX_MISSING_CHAPTERS:
            for chapter_match in chapter_letter_match:
                h1_html_tag_a = f"<{HEADERS_TO_HTML['Chapter']}>"
                h1_html_tag_b = f"</{HEADERS_TO_HTML['Chapter']}>"
                new_text = h1_html_tag_a + chapter_match[3] + ". " + chapter_match[5] + h1_html_tag_b
                if chapter_match[7] != '':
                    new_text = h1_html_tag_a + chapter_match[3] + ". " + chapter_match[5] + " - " + chapter_match[7] + h1_html_tag_b
                logger.info("%s --> %s", chapter_match[0], new_text)
                str_soup = str_soup.replace(chapter_match[0], new_text)

            most_common_tag = HEADERS_TO_HTML["Chapter"]
        else:
            logger.info("More than %s chapters are missing (%s), skipping this file", MAX_MISSING_CHAPTERS, missing_chapter)

    # Count repetitive patterns (Chapter 1, Chapter 2, Chapter 3, etc.) --> Too much work for some exceptions
    # else:
    #     for child in body_tag.children:
    #         text = child.get_text().strip()

    #         # Skip text containing an excluded word
    #         not_header_words_present = [ele for ele in NOT_HEADER_WORDS if search(r"(?i)(?<!\S)" + escape(ele) + r"[\.:]{0,1}" + r"(?!\S)", text)]           
    #         if (not_header_words_present):
    #             continue

    #         # List of header 1 keywords present at the beginning of the text (empty or one word only)
    #         header_1_keyword_first = [ele for ele in HEADER_1_NAMES_LIST if text.upper().startswith(ele)]

    #         # Search for chapter number
    #         if (header_1_keyword_first and len(text.split()) >= 2):
    #             # List of letter numbers (whole word only with eventually . or : at the end) | (?i) = case insensitive search
    #             letter_number = [ele for ele in NUMBER_DICT.keys() if search(r"(?i)(?<!\S)" + escape(ele) + r"[\.:]{0,1}" + r"(?!\S)", text.split()[1])]
    #             # List of first digits in text (with . and : characters stuck to it)
    #             digit = [ele for ele in text if match(r"(?<!\S)" + r"\d+" + r"[\.:]{0,1}" + r"(?!\S)", text.split()[1])]
    #         else:
    #             # List of letter numbers (whole word only with eventually . or : at the end) | (?i) = case insensitive search
    #             letter_number = [ele for ele in NUMBER_DICT.keys() if search(r"(?i)(?<!\S)" + escape(ele) + r"[\.:]{0,1}" + r"(?!\S)", text.split()[0])]
    #             # List of first digits in text (with . and : characters stuck to it)
    #             digit = [ele for ele in text if match(r"(?<!\S)" + r"\d+" + r"[\.:]{0,1}" + r"(?!\S)", text.split()[0])]        

    soup = BeautifulSoup(str_soup, "html.parser")
    body_tag = soup.body

    logger.info("\n------------------------ Second analysis ------------------------")
    for child in body_tag.children:
        LIST_OF_ACTIONS_LOGS = ""

        old_child = child

        # Remove empty paragraphs
        if child.get_text().strip() == "":
            # logger.info(f"Empty paragraph skipped")
            # logger.info(child.extract())
            continue

        # If title is found in the first 3 paragraphs, remove it (as it will be properly added later)
        if (child_count < 3 and child.get_text().strip() == metadata.title.strip()):
            logger.info("Found title: '%s', removing it", child.string.extract())
            continue
        if (child_count >= 3 and child.get_text().strip() == metadata.title.strip()):
            logger.info("⚠️ Found title: '%s' but NOT removing it as it's not in the first %s paragraphs", child.string.extract(), child_count)

        # If text is not a chapter but as a tag lower than h2 (h3, h4, etc.), set it as a chapter
        if (most_common_tag != '' and child.name and
            child.name == most_common_tag):
            if child.string is not None:
                child.string = child.get_text().strip()
            # logger.info(f"[{child.name} > {HEADERS_TO_HTML['Chapter']}] Set '{child}' as a chapter")
            child.string = child.get_text()
            child.name = HEADERS_TO_HTML["Chapter"]
        # elif (most_common_tag != '' and child.name and match(REG_HEADERS, child.name) and
            #   (int(child.name[1]) < int(most_common_tag[1]))):
            # logger.info(f"Found uncommon header '{child.name}', ignored")

        # Find chapter in text if required and format chapter
        if (child.name == HEADERS_TO_HTML["Chapter"] or (chapter_finder(child.get_text().strip()) and most_common_tag == '')):
            child.string = chapter_formatter(child.get_text().strip(), chapter_number)
            chapter_number += 1
            child.name = HEADERS_TO_HTML["Chapter"]

        # Count number of childs
        child_count += 1

        # Count number of words in child.get_text()
        word_count += len(child.get_text().split())

        if old_child != child:
            logger.info("%s > %s --> %s", LIST_OF_ACTIONS_LOGS, old_child, child)
            # logging.debug("%s \"%s\" --> \"%s\"", list_of_actions_logs, old_child, child)

    logger.info("Found %s paragraphs and %s words", child_count, word_count)

    # for element in soup:
        # yield element

    # 1] We have specific styles for chapters
    # 2] We already have the titles/copyrights written at the very beginning
    # 3] We have HEADER_1_NAMES_LIST to recognize chapters
    # 4] We have numbers to recognize chapters
    # 5] ? We have the length of the text to recognize chapters ?
    # 6] >>>> If first X chapters have a header keyword/number, use this detection scheme for the remaining of the document <<<<
    # 7] Remove table, table of content and other unused stuffs and warn the user

    # FOR DEBUGGING
    with open("Output.html", "w", encoding="utf-8") as file:
        file.write(soup.prettify())
    # FOR DEBUGGING

    return soup, word_count


if __name__ == "__main__":
    logger.info("Nothing to do")
    sys.exit(0)
