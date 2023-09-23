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

MAX_MISSING_CHAPTERS = 3

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