import aspose.words as aw
from pathlib import Path
from config import *
import traceback


# Find all docx files in input folder and recreate subfolders in output_folder
files_list = list(Path().glob(epub_input_folder + "/**/*.docx"))
for file in files_list:
    input_file_path = file.as_posix()
    temp_output_file_path = f"{output_folder}/{file.relative_to(*file.parts[:1]).as_posix()}"
    if (file.parents[-2] != output_folder):
        print("Working on " + input_file_path)
        Path(temp_output_file_path).parents[0].mkdir(parents=True, exist_ok=True)
        try:
            # output_file_path = temp_output_file_path.replace(".docx", "")
            output_file_path = temp_output_file_path.replace(".docx", ".epub")
            print("Output:", output_file_path)
            # temp_metadata = METADATA
            # for item in temp_metadata:
            #     if (temp_metadata[item] == ""):
            #         if (item == "creator"):
            #             list = [input("Enter value for: " + item + "\n")]
            #             temp_metadata[item] = list
            #         else:
            #             temp_metadata[item] = input("Enter value for: " + item + "\n")
            # print(temp_metadata)
            doc = aw.Document(input_file_path)
            doc.save(output_file_path)
            # work = CreateWork(output_file_path, metadata=temp_metadata, stateless=True)
            # work = CreateWork(output_file_path)
            # work.set_metadata(temp_metadata)
            # work.set_document(input_file_path)
            # work.build()
        except Exception:
            traceback.print_exc()
            print("    /!\ " + input_file_path + " failed /!\ \n")

print("\n========== Finished ==========")
variable = input('Press enter to exit')