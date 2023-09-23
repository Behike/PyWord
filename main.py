"""Main script converting docx files from INPUT_FOLDER to epub files in OUTPUT_FOLDER"""
import os
import sys
import datetime
import logging
import time
from pathlib import Path
from multiprocessing.dummy import Pool as ThreadPool
from epub_creator import create_epub
from html_parser import docx_to_html, iterate_html
from metadata_parser import parse_docx, parse_html

from Config.config import (
    INPUT_FOLDER,
    OUTPUT_FOLDER,
    DEBUG_LEVEL,
    SKIPPED_FOLDERS
)

logging.basicConfig(
        format='%(message)s',
        level=DEBUG_LEVEL,
        handlers=[
            logging.FileHandler(filename="main.log", encoding='utf-8'),
            logging.StreamHandler(sys.stdout)
        ]
    )

def path_function(file):
    """Main function to convert a docx file to epub"""
    input_docx_file = file.as_posix()
    filename = input_docx_file[input_docx_file.rfind('/')+1:input_docx_file.rfind('.')]
    temp_output_file_path = f"{OUTPUT_FOLDER}/{file.relative_to(*file.parts[:1]).as_posix()}"
    output_folder_path = temp_output_file_path[:temp_output_file_path.rfind('/')]

    if file.parents[-2] != OUTPUT_FOLDER:
        logging.info("\nWorking on %s", input_docx_file)
        Path(output_folder_path).mkdir(parents=True, exist_ok=True)
        try:
            # html_file = os.path.join(output_folder_path, filename + ".html")

            html = docx_to_html(input_docx_file)
            epub_data = parse_docx(input_docx_file)
            epub_data = parse_html(epub_data, html)
            new_soup, words_count = iterate_html(epub_data, html)

            epub_file = os.path.join(output_folder_path, f"{filename} - {words_count}.epub")
            create_epub(epub_file, epub_data, new_soup)

            if words_count == 0:
                logging.warning("No words were detected in %s (document might be a table)\n", file.name.replace("docx", ""))
            words_count = 0
        except (FileNotFoundError, PermissionError, ValueError) as e:
            logging.error(str(e))
            logging.error("    /!\\ %s failed /!\\ \n", input_docx_file)

def log_result(retval):
    """Show progress"""
    results.append(retval)
    if len(files_list)//10 == 0 or len(results) % (len(files_list)//10) == 0:
        logging.info("%d%% done", 100 * len(results) / len(files_list))


if __name__ == '__main__':
    start_time = time.time()
    logging.info("\n================================ Main script ================================")
    logging.info(datetime.datetime.now())

    # Find all doc and docx files in input folder and recreate subfolders in output_folder
    files_list = list(Path().glob(INPUT_FOLDER + "/**/*.docx"))
    files_list.extend(list(Path().glob(INPUT_FOLDER + "/**/*.doc")))

    # Skip files in a skipped_folders folder
    for i in reversed(range(len(files_list))):
        skipped_folders_in_path = [ele for ele in SKIPPED_FOLDERS if ele in (part.upper() for part in files_list[i].parts)]
        if skipped_folders_in_path:
            print("Skipping " + files_list[i].as_posix())
            files_list.remove(files_list[i])

    pool = ThreadPool(1)

    results = []
    for item in files_list:
        pool.apply_async(path_function, args=[item], callback=log_result)

    # Close the pool and wait for the work to finish
    pool.close()
    pool.join()

    logging.info("\n==================== Finished in %ss ====================\n\n", (time.time() - start_time))
    variable = input('Press enter to exit')
    