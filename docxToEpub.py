from glob import glob
import re
import pypandoc
from updateablezipfile import UpdateableZipFile
from zipfile import ZipFile
from docx import Document
from docx.enum.style import WD_STYLE_TYPE
from docx.enum.section import WD_ORIENTATION
from pathlib import Path
from re import compile, search, escape, match, IGNORECASE
from config import *
import traceback, logging, sys
import time, datetime

#######################################################################
### This script is to re-add removed chapters after the main script ###
#######################################################################

logging.basicConfig(
        format='%(message)s',
        level=debug_level,
        handlers=[
            logging.FileHandler(filename="addChapter.log", encoding='utf-8'),
            logging.StreamHandler(sys.stdout)
        ]
    )

def docxToEpub(input_docx, output_epub):
    # Open document to retrieve title and author
    document = Document(input_docx)
    
    # Create output folder if file is created only
    Path(output_epub).parents[0].mkdir(parents=True, exist_ok=True)

    if (output_epub.lower().endswith('.doc')):
        output_epub = output_epub.replace(output_epub[output_epub.rfind('.')+1:], 'docx')
        input_docx = input_docx.replace(input_docx[input_docx.rfind('.')+1:], 'docx')
    document.save(output_epub)

    epub_file_path = output_epub.replace(output_epub[output_epub.rfind('.')+1:], 'epub')
    print(epub_file_path)
    # Convert to epub
    pypandoc.convert_file(
        output_epub,
        'epub',
        outputfile=epub_file_path,
        extra_args=[
            '--metadata',
            'title={0}'.format(document.core_properties.title),
            '--metadata',
            'creator={0}'.format(document.core_properties.author),
            '--epub-embed-font={0}'.format('Style/Cambria-Font.ttf'),
            '--epub-embed-font={0}'.format('Style/Palatino Linotype.ttf'),
            '--css=Style/default.css',
            '--top-level-division=chapter'
            # '--standalone=false',
            # '--toc'
        ]
    )

    toc_file_path = 'EPUB/toc.ncx'
    content_file_path = 'EPUB/content.opf'
    nav_file_path = 'EPUB/nav.xhtml'
    title_page_file_path = 'EPUB/text/title_page.xhtml'
    ch001_file_path = 'EPUB/text/ch001.xhtml'
    toc_data = ''
    content_data = ''
    nav_data = ''
    title_page_data = ''

    # Read and modify files content in epub 
    with ZipFile(epub_file_path, 'r', metadata_encoding='utf-8') as epub:
        epub.printdir()
        toc_data = epub.read(toc_file_path).decode("utf-8") 
        
        ## TOC file --> Remove ch001
        # Add playOrder and class elements to each navPoint except first (0)
        toc_data = re.sub(r'navPoint-([1-9]{1}\d*)"', r'navPoint-\1" playOrder="\1" class="chapter"', toc_data)
        # Remove navPoint-0 element (wrong title)
        # toc_file = re.sub(r'\s+<navPoint id="navPoint-0" playOrder="0" class="chapter">.*?</navPoint>', '', toc_file, flags=re.MULTILINE|re.DOTALL)
        toc_data = re.sub(r'\s+<navPoint id="navPoint-0">.*?</navPoint>', '', toc_data, flags=re.MULTILINE|re.DOTALL)
        # Replace first navPoint class (chapter --> titlepage)
        toc_data = toc_data.replace('<navPoint id="navPoint-1" playOrder="1" class="chapter">', '<navPoint id="navPoint-1" playOrder="1" class="titlepage">')
        # print(toc_data)

        ## Content file --> Remove ch001 lines
        content_data = epub.read(content_file_path).decode("utf-8") 
        content_data = re.sub(r'\s+<item id="ch001_xhtml" href="text/ch001\.xhtml" media-type="application/xhtml\+xml" />', '', content_data, flags=re.MULTILINE)
        content_data = re.sub(r'\s+<itemref idref="ch001_xhtml" />', '', content_data, flags=re.MULTILINE)       
        # print(content_data)

        ## Nav file --> Remove ch001 part
        nav_data = epub.read(nav_file_path).decode("utf-8") 
        nav_data = re.sub(r'<li id="toc-li-1"><a href="text/ch001.xhtml">.*?</a></li>', '', nav_data, flags=re.MULTILINE|re.DOTALL)
        # print(nav_data)

        ## Title page --> Replace paragraph with the one from ch001.xhtml
        title_page_data = epub.read(title_page_file_path).decode("utf-8")
        ch001_data = epub.read(ch001_file_path).decode("utf-8")
        ch001_data = re.findall(r'<p>.*?</p>', ch001_data, flags=re.MULTILINE|re.DOTALL)
        # Remove duplicate title paragraph
        title_to_remove = '<p>' + document.core_properties.title.strip().lower() + '</p>'
        filename_to_remove = '<p>' + input_docx[input_docx.rfind('/')+1:input_docx.rfind('-')-1].lower() + '</p>'

        for i in reversed(range(len(ch001_data))):
            if (title_to_remove == ch001_data[i].strip().lower()):
                ch001_data.remove(ch001_data[i])
                logging.debug('Removed title paragraph')
            elif (filename_to_remove == ch001_data[i].strip().lower()):
                ch001_data.remove(ch001_data[i])
                logging.debug('Removed title (filename) paragraph')
            else:
                logging.info('Nothing in ch001')

        if (title_to_remove in title_page_data.lower()):
            title_page_data = title_page_data.replace(title_to_remove, '')
            logging.debug('Removed title paragraph')
        elif (filename_to_remove in title_page_data.lower()):
            title_page_data = title_page_data.replace(filename_to_remove, '')
            logging.debug('Removed title (filename) paragraph')
        else:
            logging.debug('No duplicate title found')

        # Add subtitle id to title paragraph to styled it differently
        if ('\n'.join(ch001_data).find('<p>Copyright') != -1 or '\n'.join(ch001_data).find('<p class="subtitle">Copyright') != -1):
            logging.debug('Using ch001 Copyrights')
            ch001_data = ch001_data[0].replace('<p>', '<p id="subtitle">')
        elif (title_page_data.find('<p>Copyright') != -1 or title_page_data.find('<p class="subtitle">Copyright') != -1):
            logging.debug('Using title_page Copyrights')
            title_page_data = title_page_data.replace('<p>', '<p id="subtitle">')
        else:
            logging.error('No copyright found')

        if (type(ch001_data) is list):
            ch001_data = '\n'.join(ch001_data)

        if (title_page_data.find('<p class=""></p>') == -1):
            logging.error("'<p class=""></p>' could not be found in title_page")
        else:
            title_page_data = title_page_data.replace('<p class=""></p>', ch001_data)

    # Update archive (epub) with modified files
    with UpdateableZipFile(epub_file_path, "a") as o:
        # Overwrite toc file
        o.writestr(toc_file_path, str.encode(toc_data))
        # Overwrite content file
        o.writestr(content_file_path, str.encode(content_data))
        # Overwrite nav file
        o.writestr(nav_file_path, str.encode(nav_data))

        # Remove ch001.xhtml from text folder
        o.remove_file(ch001_file_path)
        # Overwrite title_page.xhtml
        o.writestr(title_page_file_path, str.encode(title_page_data))



if __name__ == '__main__':
    start_time = time.time()
    logging.info("\n================================ docx to epub script ================================")
    logging.info(datetime.datetime.now())

    # Find all docx files in input input_chapters_folder and recreate subfolders in output_chapters_folder
    files_list = list(Path().glob(input_chapters_folder + "/**/*.doc*"))

    # Skip files in a skipped_folders folder
    for i in reversed(range(len(files_list))):
        skipped_folders_in_path = [ele for ele in skipped_folders if ele in (part.upper() for part in files_list[i].parts)]
        if (skipped_folders_in_path):
            print("Skipping " + files_list[i].as_posix())
            files_list.remove(files_list[i])

    for file in files_list:
        input_file_path = file.as_posix()
        output_file_path = f"{output_chapters_folder}/{file.relative_to(*file.parts[:1]).as_posix()}"
        if (file.parents[-2] != output_chapters_folder):
            logging.info("\nWorking on %s", input_file_path)
            try:
                docxToEpub(input_file_path, output_file_path)
            except Exception:
                traceback.print_exc()
                logging.error("    /!\ %s failed /!\ \n", input_file_path)

    logging.info("\n==================== Finished in %ss ====================\n\n\n", (time.time() - start_time))
    variable = input('Press enter to exit')