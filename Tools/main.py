import datetime
import os
from pathlib import Path
import sys
from epub_creator import create_epub
from html_parser import docx_to_html, iterate_html
from metadata_parser import parse_docx, parse_html
from config import *
import traceback, logging
import time, datetime

logging.basicConfig(
        format='%(message)s',
        level=DEBUG_LEVEL,
        handlers=[
            logging.FileHandler(filename="main.log", encoding='utf-8'),
            logging.StreamHandler(sys.stdout)
        ]
    )
word_count = 0


if __name__ == '__main__':     
    start_time = time.time()
    logging.info("\n================================ Main script ================================")
    logging.info(datetime.datetime.now())

    # Find all doc and docx files in input folder and recreate subfolders in output_folder
    files_list = list(Path().glob(INPUT_FOLDER + "/**/*.docx"))
    files_list.extend(list(Path().glob(INPUT_FOLDER + "/**/*.doc")))

    for file in files_list:
        input_docx_file = file.as_posix()
        filename = input_docx_file[input_docx_file.rfind('/')+1:input_docx_file.rfind('.')]
        temp_output_file_path = f"{OUTPUT_FOLDER}/{file.relative_to(*file.parts[:1]).as_posix()}"
        output_folder_path = temp_output_file_path[:temp_output_file_path.rfind('/')]
        
        if (file.parents[-2] != OUTPUT_FOLDER):
            logging.info("\nWorking on %s", input_docx_file)
            Path(output_folder_path).mkdir(parents=True, exist_ok=True)
            try:
                file_extension = input_docx_file[input_docx_file.rfind('.')+1:]

                # print(f"Converting {filename}")
                # print("output_folder_path:", output_folder_path)

                html_file = os.path.join(output_folder_path, filename + ".html")
                # print("html_file:", html_file)

                html = docx_to_html(input_docx_file)
                epub_data = parse_docx(input_docx_file)
                epub_data = parse_html(epub_data, html)
                new_soup, words_count = iterate_html(epub_data, html)

                epub_file = os.path.join(output_folder_path, f"{filename} - {words_count}.epub")
                # print("epub_file: ", epub_file)
                create_epub(epub_file, epub_data, new_soup)
                
                if (words_count == 0):
                    logging.warning("No words were detected in %s (document might be a table)\n", file.name.replace("docx", ""))
                words_count = 0
            except Exception:
                traceback.print_exc()
                logging.error("    /!\ %s failed /!\ \n", input_docx_file)

    logging.info("\n==================== Finished in %ss ====================\n\n\n", (time.time() - start_time))
    variable = input('Press enter to exit')