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

def addChaptersToDocuments(input_docx, output_docx):
    document = Document(input_docx)
    chapter_number = 1
    has_been_modified = False

    # If more than 5 correct Heading 1 are detected, skip the remaining of the document
    clean_counter = 0

    for para in document.paragraphs:
        para_text = para.text.strip()
        para_text_old = para_text

        if (para_text != "" and para.style.name == 'Heading 1'):
            header_1_keyword_first = [ele for ele in header_1_names_list if para_text.upper().startswith(ele)]
            if (header_1_keyword_first):
                logging.debug("Header 1 correct: " + para_text)    
                clean_counter = clean_counter + 1
                
            else:
                if (clean_counter < 5):
                    para.text = header_1_names_list[0].capitalize() + " " + str(chapter_number) + " - " + para_text
                    chapter_number = chapter_number + 1
                    has_been_modified = True
                    logging.debug("[UPDATED] " + para_text_old + " --> " + para.text)
                else:
                    logging.debug("[NOT UPDATED] " + para_text_old + " --> " + para.text)

    # Save document if updated
    if (has_been_modified):
        # Create output folder if file is created only
        Path(output_docx).parents[0].mkdir(parents=True, exist_ok=True)

        if (output_docx.lower().endswith('.doc')):
            output_docx = output_docx.replace(output_docx[output_docx.rfind('.')+1:], 'docx')
            input_docx = input_docx.replace(input_docx[input_docx.rfind('.')+1:], 'docx')
        document.save(output_docx)
    
        epub_file_path = output_docx.replace(output_docx[output_docx.rfind('.')+1:], 'epub')
        print(epub_file_path)

        # Convert to epub
        pypandoc.convert_file(
            output_docx,
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
            ch001_data = re.search(r'<p>Copyright.*?</p>', ch001_data, flags=re.MULTILINE|re.DOTALL)
            # Add subtitle id to title paragraph to styled it differently
            ch001_data = ch001_data[0].replace('<p>', '<p id="subtitle">')
            print(ch001_data)
            title_page_data = title_page_data.replace('<p class=""></p>', ch001_data)
            print(title_page_data)

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
    else:
        logging.warning('No conversion was made as no modifications ')


if __name__ == '__main__':
    start_time = time.time()
    logging.info("\n================================ Add chapter script ================================")
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
                addChaptersToDocuments(input_file_path, output_file_path)
            except Exception:
                traceback.print_exc()
                logging.error("    /!\ %s failed /!\ \n", input_file_path)

    logging.info("\n==================== Finished in %ss ====================\n\n\n", (time.time() - start_time))
    variable = input('Press enter to exit')