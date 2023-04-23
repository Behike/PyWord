from docx.shared import Pt, Mm, Inches, RGBColor
from docx.enum.style import WD_STYLE_TYPE
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.section import WD_ORIENTATION

# Choose log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
debug_level = "DEBUG"

# Folder where to search for/save files
input_folder = "0 - Input"
output_folder = "0 - Output"

# A chapter/Heading 1 can be recognized if it starts with one of header_1_names_list
# word and the whole paragraph is at most 75 characters long
CHAPTER_MAX_LENGTH = 75

# First item is the one written if no header is present
header_1_names_list = [
    "CHAPTER",
    "EPILOGUE",
    "PROLOGUE"
]

# Items that should not be capitalized in headings/titles
capitalize_words_list = [
    "of",
    "in",
    "and",
    "a"
]
    
## Styles definition, cannot add new properties from here for now
# Title
title_paragraph_alignment = WD_ALIGN_PARAGRAPH.CENTER
title_paragraph_page_break_before = True
title_paragraph_space_before = Pt(45)
title_paragraph_space_after = Pt(45)
title_font_name = "Cambria"
title_font_size = Pt(36)
title_font_color = RGBColor(0x0,0x0,0x0)
title_font_bold = False
title_font_italic = False
title_font_underline = False

# Heading 1
heading_1_paragraph_alignment = WD_ALIGN_PARAGRAPH.CENTER
heading_1_paragraph_page_break_before = True
heading_1_paragraph_space_before = Pt(45)
heading_1_paragraph_space_after = Pt(45)
heading_1_font_name = "Palatino Linotype"
heading_1_font_size = Pt(36)
heading_1_font_color = RGBColor(0x0,0x0,0x0)
heading_1_font_bold = False
heading_1_font_italic = False
heading_1_font_underline = False

# Normal
normal_paragraph_alignment = WD_ALIGN_PARAGRAPH.LEFT
normal_paragraph_first_line_indent = Pt(0)
normal_paragraph_left_indent = Pt(0)
normal_paragraph_right_indent = Pt(0)
normal_paragraph_space_before = Pt(0)
normal_paragraph_space_after = Pt(6)
normal_paragraph_page_break_before = False
normal_font_name = "Palatino Linotype"
normal_font_size = Pt(10)
normal_font_color = RGBColor(0x0,0x0,0x0)
normal_font_bold = None
normal_font_italic = None
normal_font_underline = None

# Subtitle (inherits other properties from Normal)
subtitle_inherits_from = "Normal"
subtitle_paragraph_alignment = WD_ALIGN_PARAGRAPH.CENTER
subtitle_paragraph_space_after = Pt(45)
subtitle_font_name = "Palatino Linotype"
subtitle_font_size = Pt(9)
subtitle_font_bold = False
subtitle_font_italic = False
subtitle_font_underline = False

## Section configurations
# Page
page_orientation = WD_ORIENTATION.PORTRAIT
page_width = Mm(210)
page_height = Mm(297)
top_margin = Inches(1)
bottom_margin = Inches(1)
left_margin = Inches(1)
right_margin = Inches(1)
# Header/Footer
keep_headers = False
keep_footers = False

def copyrightText(created_year, author):
    copyright_text = "Copyright © " + str(created_year) + " " + author + "\nAll rights reserved. No parts of this publication may be reproduced, \
stored in a retrieval system, or transmitted in any form or by any means, electronic, mechanical, photocopying, \
recording, or otherwise, without the prior written permission of the copyright owner.\nThis book is sold subject \
to the condition that it shall not, by way of trade or otherwise, be lent, resold, hired out, or otherwise circulated \
without the publisher’s prior consent in any form of binding or cover other than that in which it is published and \
without a similar condition including this condition being imposed on the subsequent purchaser. Under no circumstances \
may any part of this book be photocopied for resale.\nThis is a work of fiction. Any similarity between the characters \
and situations within its pages and places or persons, living or dead, is unintentional and co-incidental."
    return copyright_text

number_dict = {
    "ONE": 1,
    "TWO": 2,
    "THREE": 3,
    "FOUR": 4,
    "FIVE": 5,
    "SIX": 6,
    "SEVEN": 7,
    "EIGHT": 8,
    "NINE": 9,
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
}

# If one of the following words is present in a sentence, the paragraph won't become a header
not_header_words = [
    'minute',
    'minutes',
    'hour',
    'hours',
    'week',
    'weeks',
    'day',
    'days',
    'month',
    'months',
    'year',
    'years'
]

# docxToEpub configuration
epub_input_folder = "0 - Input EPUB"
METADATA = {
    "title": "gtg",
    "language": "en",
    "creator": "",
    "rights": "All rights reserved.",
}
# METADATA = {
#     "identifier": "",
#     "title": "",
#     "description": "",
#     "language": "en",
#     "creator": "",
#     "rights": "All rights reserved.",
#     "long_rights": ["The right of the creator to be identified as the author of the Work has been asserted by them in accordance with the Copyright, Designs and Patents Act 1988. This creator supports copyright. Copyright gives creators space to explore and provides for their long-term ability to sustain themselves from their work. Thank you for buying this work and for complying with copyright laws by not reproducing, scanning, or distributing any part of it without permission. Your support will contribute to future works by the creator."],
#     "publisher": "Qwyre Publishing",
#     "publisher_uri": "https://qwyre.com",
#     "work-uri": "https://gavinchait.com",
#     "date": "2017-07-23",
#     "subject": ["science fiction", "african mythology"]
# }