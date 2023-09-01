# Get docx infos
import os
from docx import Document
# Convert docx to html
from pydocx import PyDocX
# Edit html
from bs4 import BeautifulSoup, NavigableString
# Convert html to epub
import pypub
# Import config
import sys
sys.path.append( '../' )
from config import *


# file = "A Mother's Joy"
file = "Test - Formatted"
docx_file = file + '.docx'
html_file = file + '.html'
epub_file = file + '.epub'

# Retrieve docx infos
document = Document(docx_file)
title = document.core_properties.title
author = document.core_properties.author
created = document.core_properties.created
created_year = "" if type(created) == type(None) else created.year

if (title == ""):
    title = 'No title'

print(title, author)
# Convert docx to html
html = PyDocX.to_html(docx_file)

## Edit html
soup = BeautifulSoup(html, 'html.parser')
## Edit head
head_tag = soup.head

### Add title
title_tag = soup.new_tag('h1')
title_tag.string = title
head_tag.append(title_tag)
### Add subtitle
subtitle_tag = soup.new_tag('h3')
subtitle_tag.string = copyrightText(created_year, author)
head_tag.append(subtitle_tag)
headers_list = soup.find_all('h1')

# Save html string variable into a file
with open(html_file, 'w', encoding="utf-8") as f:
    f.write(soup.prettify())

epub = pypub.Epub(title, creator=author, language='en', cover='cover.png', css_paths=['styles.css'])

for header in headers_list:
    chapter_text = ''
    while header.next_sibling != None and header.next_sibling.name != 'h1':
        chapter_text += str(header.next_sibling)
        print(header.next_sibling)
        header.next_sibling.extract()
    
    epub.add_chapter(pypub.create_chapter_from_html(chapter_text.encode(), header.text))
    # epub.add_chapter(chapter_text.encode(), header.text)
    print('Added chapter:', header.text)

# If epub_file already exists, delete it
if os.path.exists(epub_file):
    os.remove(epub_file)
    print('Removed old epub file')
    
epub.create(epub_file)