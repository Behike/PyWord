import pypandoc
from docx import Document

from pathlib import Path
from config import *
import traceback

file = 'Season 1.docx'

document = Document(file)
print('--epub-metadata title={0} creator={1} language={2}'.format(document.core_properties.title, document.core_properties.author, 'en-US'))

print(file[file.rfind('.')+1:])
# pypandoc.convert_file(
#     file,
#     'epub',
#     outputfile='Season 1.epub',
#     extra_args=[
#         '--metadata',
#         'title={0}'.format(document.core_properties.title),
#         '--metadata',
#         'creator={0}'.format(document.core_properties.author)
#     ]
# )
    # extra_args='--epub-metadata title={0} creator={1} language={2}'.format(document.core_properties.title, document.core_properties.author, 'en-US'))

# # Find all docx files in input folder and recreate subfolders in output_chapters_folder
# files_list = list(Path().glob(epub_input_folder + "/**/*.docx"))
# for file in files_list:
#     input_file_path = file.as_posix()
#     temp_output_file_path = f"{output_chapters_folder}/{file.relative_to(*file.parts[:1]).as_posix()}"
#     if (file.parents[-2] != output_chapters_folder):
#         print("Working on " + input_file_path)
#         Path(temp_output_file_path).parents[0].mkdir(parents=True, exist_ok=True)
#         try:
#             # output_file_path = temp_output_file_path.replace(".docx", "")
#             output_file_path = Path(temp_output_file_path).parents[0]
#             print("Output:", output_file_path)
#             temp_metadata = METADATA
#             for item in temp_metadata:
#                 if (temp_metadata[item] == ""):
#                     if (item == "creator"):
#                         list = [input("Enter value for: " + item + "\n")]
#                         temp_metadata[item] = list
#                     else:
#                         temp_metadata[item] = input("Enter value for: " + item + "\n")
#             print(temp_metadata)
#             # work = CreateWork(output_file_path, metadata=temp_metadata, stateless=True)
#             work = CreateWork(output_file_path)
#             work.set_metadata(temp_metadata)
#             work.set_document(input_file_path)
#             work.build()
#             if (not work.validate()):
#                 print("    /!\ Created EPUB file is not standards compliant /!\ \n")
#         except Exception:
#             traceback.print_exc()
#             print("    /!\ " + input_file_path + " failed /!\ \n")

print("\n========== Finished ==========")
variable = input('Press enter to exit')