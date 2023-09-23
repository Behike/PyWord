from docx.shared import Pt, Mm, Inches, RGBColor
from docx.enum.style import WD_STYLE_TYPE
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.section import WD_ORIENTATION

# Choose log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
DEBUG_LEVEL = "INFO"

## Folder where to search for/save files
# Skip files in those folders (case insensitive)
SKIPPED_FOLDERS = ["PAST", "OLD"]
# Main script
INPUT_FOLDER = "0 - Input"
OUTPUT_FOLDER = "0 - Output"
# Missing chapters script
INPUT_CHAPTERS_FOLDER = "0 - Output"
OUTPUT_CHAPTERS_FOLDER = "0 - Output chapters"
# Docx to Epub script
INPUT_EPUB_FOLDER = "0 - Output"
OUTPUT_EPUB_FOLDER = "0 - Output EPUB"

# A chapter/Heading 1 can be recognized if it starts with one of header_1_names_list
# word and the whole paragraph is at most 30 characters long
CHAPTER_MAX_LENGTH = 30

# Maximum of characters since the beginning for a h3/Heading 3 to be considered as a subtitle
SUBTITLE_MAX_SEARCH = 40

# First item is the one written if no header is present (case insensitive)
HEADER_1_NAMES_LIST = [
    "CHAPTER",
    "EPILOGUE",
    "PROLOGUE",
    "ACKNOWLEDGMENT",
    "ACKNOWLEDGMENTS",
    "FOREWORD",
]

# Items that should not be capitalized in headings/titles
CAPITALIZE_WORDS_LIST = ["of", "in", "and", "a"]

## Styles definition, cannot add new properties from here for now
# Title
TITLE_PARAGRAPH_ALIGNMENT = WD_ALIGN_PARAGRAPH.CENTER
TITLE_PARAGRAPH_PAGE_BREAK_BEFORE = True
TITLE_PARAGRAPH_SPACE_BEFORE = Pt(45)
TITLE_PARAGRAPH_SPACE_AFTER = Pt(45)
TITLE_FONT_NAME = "Cambria"
TITLE_FONT_SIZE = Pt(36)
TITLE_FONT_COLOR = RGBColor(0x0, 0x0, 0x0)
TITLE_FONT_BOLD = False
TITLE_FONT_ITALIC = False
TITLE_FONT_UNDERLINE = False

# Heading 1
HEADING_1_PARAGRAPH_ALIGNMENT = WD_ALIGN_PARAGRAPH.CENTER
HEADING_1_PARAGRAPH_PAGE_BREAK_BEFORE = True
HEADING_1_PARAGRAPH_SPACE_BEFORE = Pt(45)
HEADING_1_PARAGRAPH_SPACE_AFTER = Pt(45)
HEADING_1_FONT_NAME = "Palatino Linotype"
HEADING_1_FONT_SIZE = Pt(36)
HEADING_1_FONT_COLOR = RGBColor(0x0, 0x0, 0x0)
HEADING_1_FONT_BOLD = False
HEADING_1_FONT_ITALIC = False
HEADING_1_FONT_UNDERLINE = False

# Normal
NORMAL_PARAGRAPH_ALIGNMENT = WD_ALIGN_PARAGRAPH.LEFT
NORMAL_PARAGRAPH_FIRST_LINE_INDENT = Pt(0)
NORMAL_PARAGRAPH_LEFT_INDENT = Pt(0)
NORMAL_PARAGRAPH_RIGHT_INDENT = Pt(0)
NORMAL_PARAGRAPH_SPACE_BEFORE = Pt(0)
NORMAL_PARAGRAPH_SPACE_AFTER = Pt(6)
NORMAL_PARAGRAPH_PAGE_BREAK_BEFORE = False
NORMAL_FONT_NAME = "Palatino Linotype"
NORMAL_FONT_SIZE = Pt(10)
NORMAL_FONT_COLOR = RGBColor(0x0, 0x0, 0x0)
NORMAL_FONT_BOLD = None
NORMAL_FONT_ITALIC = None
NORMAL_FONT_UNDERLINE = None

# Subtitle (inherits other properties from Normal)
SUBTITLE_INHERITS_FROM = "Normal"
SUBTITLE_PARAGRAPH_ALIGNMENT = WD_ALIGN_PARAGRAPH.CENTER
SUBTITLE_PARAGRAPH_SPACE_AFTER = Pt(45)
SUBTITLE_FONT_NAME = "Palatino Linotype"
SUBTITLE_FONT_SIZE = Pt(9)
SUBTITLE_FONT_BOLD = False
SUBTITLE_FONT_ITALIC = False
SUBTITLE_FONT_UNDERLINE = False

## Section configurations
# Page
PAGE_ORIENTATION = WD_ORIENTATION.PORTRAIT
PAGE_WIDTH = Mm(210)
PAGE_HEIGHT = Mm(297)
TOP_MARGIN = Inches(1)
BOTTOM_MARGIN = Inches(1)
LEFT_MARGIN = Inches(1)
RIGHT_MARGIN = Inches(1)
# Header/Footer
KEEP_HEADERS = False
KEEP_FOOTERS = False


def copyright_text(created_year, author):
    """Create and return a copyright text after adding year of creation and author name"""
    text = (
        "Copyright © "
        + str(created_year)
        + " "
        + author
        + "\nAll rights reserved. No parts of this publication may be reproduced, \
stored in a retrieval system, or transmitted in any form or by any means, electronic, mechanical, photocopying, \
recording, or otherwise, without the prior written permission of the copyright owner.\nThis book is sold subject \
to the condition that it shall not, by way of trade or otherwise, be lent, resold, hired out, or otherwise circulated \
without the publisher’s prior consent in any form of binding or cover other than that in which it is published and \
without a similar condition including this condition being imposed on the subsequent purchaser. Under no circumstances \
may any part of this book be photocopied for resale.\nThis is a work of fiction. Any similarity between the characters \
and situations within its pages and places or persons, living or dead, is unintentional and co-incidental."
    )
    return text


NUMBER_DICT = {
    "TEN": 10,
    "ELEVEN": 11,
    "TWELVE": 12,
    "THIRTEEN": 13,
    "FOURTEEN": 14,
    "FIFTEEN": 15,
    "SIXTEEN": 16,
    "SEVENTEEN": 17,
    "EIGHTEEN": 18,
    "NINETEEN": 19,
    "TWENTY": 20,
    "TWENTY-ONE": 21,
    "TWENTY-TWO": 22,
    "TWENTY-THREE": 23,
    "TWENTY-FOUR": 24,
    "TWENTY-FIVE": 25,
    "TWENTY-SIX": 26,
    "TWENTY-SEVEN": 27,
    "TWENTY-EIGHT": 28,
    "TWENTY-NINE": 29,
    "THIRTY": 30,
    "THIRTY-ONE": 31,
    "THIRTY-TWO": 32,
    "THIRTY-THREE": 33,
    "THIRTY-FOUR": 34,
    "THIRTY-FIVE": 35,
    "THIRTY-SIX": 36,
    "THIRTY-SEVEN": 37,
    "THIRTY-EIGHT": 38,
    "THIRTY-NINE": 39,
    "FORTY": 40,
    "FORTY-ONE": 41,
    "FORTY-TWO": 42,
    "FORTY-THREE": 43,
    "FORTY-FOUR": 44,
    "FORTY-FIVE": 45,
    "FORTY-SIX": 46,
    "FORTY-SEVEN": 47,
    "FORTY-EIGHT": 48,
    "FORTY-NINE": 49,
    "FIFTY": 50,
    "FIFTY-ONE": 51,
    "FIFTY-TWO": 52,
    "FIFTY-THREE": 53,
    "FIFTY-FOUR": 54,
    "FIFTY-FIVE": 55,
    "FIFTY-SIX": 56,
    "FIFTY-SEVEN": 57,
    "FIFTY-EIGHT": 58,
    "FIFTY-NINE": 59,
    "SIXTY": 60,
    "SIXTY-ONE": 61,
    "SIXTY-TWO": 62,
    "SIXTY-THREE": 63,
    "SIXTY-FOUR": 64,
    "SIXTY-FIVE": 65,
    "SIXTY-SIX": 66,
    "SIXTY-SEVEN": 67,
    "SIXTY-EIGHT": 68,
    "SIXTY-NINE": 69,
    "SEVENTY": 70,
    "SEVENTY-ONE": 71,
    "SEVENTY-TWO": 72,
    "SEVENTY-THREE": 73,
    "SEVENTY-FOUR": 74,
    "SEVENTY-FIVE": 75,
    "SEVENTY-SIX": 76,
    "SEVENTY-SEVEN": 77,
    "SEVENTY-EIGHT": 78,
    "SEVENTY-NINE": 79,
    "EIGHTY": 80,
    "EIGHTY-ONE": 81,
    "EIGHTY-TWO": 82,
    "EIGHTY-THREE": 83,
    "EIGHTY-FOUR": 84,
    "EIGHTY-FIVE": 85,
    "EIGHTY-SIX": 86,
    "EIGHTY-SEVEN": 87,
    "EIGHTY-EIGHT": 88,
    "EIGHTY-NINE": 89,
    "NINETY": 90,
    "NINETY-ONE": 91,
    "NINETY-TWO": 92,
    "NINETY-THREE": 93,
    "NINETY-FOUR": 94,
    "NINETY-FIVE": 95,
    "NINETY-SIX": 96,
    "NINETY-SEVEN": 97,
    "NINETY-EIGHT": 98,
    "NINETY-NINE": 99,
    "ONE HUNDRED": 100,
    "TWENTY ONE": 21,
    "TWENTY TWO": 22,
    "TWENTY THREE": 23,
    "TWENTY FOUR": 24,
    "TWENTY FIVE": 25,
    "TWENTY SIX": 26,
    "TWENTY SEVEN": 27,
    "TWENTY EIGHT": 28,
    "TWENTY NINE": 29,
    "THIRTY ONE": 31,
    "THIRTY TWO": 32,
    "THIRTY THREE": 33,
    "THIRTY FOUR": 34,
    "THIRTY FIVE": 35,
    "THIRTY SIX": 36,
    "THIRTY SEVEN": 37,
    "THIRTY EIGHT": 38,
    "THIRTY NINE": 39,
    "FORTY ONE": 41,
    "FORTY TWO": 42,
    "FORTY THREE": 43,
    "FORTY FOUR": 44,
    "FORTY FIVE": 45,
    "FORTY SIX": 46,
    "FORTY SEVEN": 47,
    "FORTY EIGHT": 48,
    "FORTY NINE": 49,
    "FIFTY ONE": 51,
    "FIFTY TWO": 52,
    "FIFTY THREE": 53,
    "FIFTY FOUR": 54,
    "FIFTY FIVE": 55,
    "FIFTY SIX": 56,
    "FIFTY SEVEN": 57,
    "FIFTY EIGHT": 58,
    "FIFTY NINE": 59,
    "SIXTY ONE": 61,
    "SIXTY TWO": 62,
    "SIXTY THREE": 63,
    "SIXTY FOUR": 64,
    "SIXTY FIVE": 65,
    "SIXTY SIX": 66,
    "SIXTY SEVEN": 67,
    "SIXTY EIGHT": 68,
    "SIXTY NINE": 69,
    "SEVENTY ONE": 71,
    "SEVENTY TWO": 72,
    "SEVENTY THREE": 73,
    "SEVENTY FOUR": 74,
    "SEVENTY FIVE": 75,
    "SEVENTY SIX": 76,
    "SEVENTY SEVEN": 77,
    "SEVENTY EIGHT": 78,
    "SEVENTY NINE": 79,
    "EIGHTY ONE": 81,
    "EIGHTY TWO": 82,
    "EIGHTY THREE": 83,
    "EIGHTY FOUR": 84,
    "EIGHTY FIVE": 85,
    "EIGHTY SIX": 86,
    "EIGHTY SEVEN": 87,
    "EIGHTY EIGHT": 88,
    "EIGHTY NINE": 89,
    "NINETY ONE": 91,
    "NINETY TWO": 92,
    "NINETY THREE": 93,
    "NINETY FOUR": 94,
    "NINETY FIVE": 95,
    "NINETY SIX": 96,
    "NINETY SEVEN": 97,
    "NINETY EIGHT": 98,
    "NINETY NINE": 99,
    "ONE": 1,
    "TWO": 2,
    "THREE": 3,
    "FOUR": 4,
    "FIVE": 5,
    "SIX": 6,
    "SEVEN": 7,
    "EIGHT": 8,
    "NINE": 9,
}

# If one of the following words is present in a sentence, the paragraph won't become a header
NOT_HEADER_WORDS = [
    "minute",
    "minutes",
    "hour",
    "hours",
    "week",
    "weeks",
    "day",
    "days",
    "month",
    "months",
    "year",
    "years",
]

# docxToEpub configuration
TOC_FILE_PATH = "EPUB/toc.ncx"
CONTENT_FILE_PATH = "EPUB/content.opf"
NAV_FILE_PATH = "EPUB/nav.xhtml"
TEXT_FOLDER = "EPUB/text/"
TITLE_PAGE_FILE_PATH = TEXT_FOLDER + "title_page.xhtml"
CH00X_FILE_PATH = TEXT_FOLDER + "ch00{0}.xhtml"

# New configurations
TEMPLATES = "Templates/"
MAX_MISSING_CHAPTERS = 3