from docx import Document
from docx.enum.style import WD_STYLE_TYPE
from docx.enum.section import WD_ORIENTATION
from pathlib import Path
from re import compile, search, escape, match, IGNORECASE
from config import *
import traceback, logging
import time

#######################################################################
### This script is to re-add removed chapters after the main script ###
### So the "output_folder" is the input of this script              ###
#######################################################################

logging.basicConfig(format='%(message)s', level=debug_level)

def addChaptersToDocuments(input, output):
    document = Document(input)
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
        document.save(output)

if __name__ == '__main__':
    start_time = time.time()

    # Find all docx files in input output_folder and recreate subfolders in output_chapters_folder
    files_list = list(Path().glob(output_folder + "/**/*.docx"))
    for file in files_list:
        input_file_path = file.as_posix()
        output_file_path = f"{output_chapters_folder}/{file.relative_to(*file.parts[:1]).as_posix()}"
        if (file.parents[-2] != output_chapters_folder):
            logging.info("\nWorking on %s", input_file_path)
            Path(output_file_path).parents[0].mkdir(parents=True, exist_ok=True)
            try:
                addChaptersToDocuments(input_file_path, output_file_path)
            except Exception:
                traceback.print_exc()
                logging.error("    /!\ %s failed /!\ \n", input_file_path)

    logging.info("\n========== Finished in %ss ==========", (time.time() - start_time))
    variable = input('Press enter to exit')