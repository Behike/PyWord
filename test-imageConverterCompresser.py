from PIL import Image
from glob import glob
from pathlib import Path
from config import *
import traceback

def convertImage(input, output):
    im = Image.open(input)
    rgb_im = im.convert('RGB')
    rgb_im.save(output)

# Find all image files in input folder and recreate subfolders in output_folder
globs = glob(input_folder + "/**/*.jpg") + glob(input_folder + "/**/*.jpeg") + glob(input_folder + "/**/*.png")
files_list = list(globs)

for file in files_list:
    input_file_path = file.as_posix()
    temp_output_file_path = f"{output_folder}/{file.relative_to(*file.parts[:1]).as_posix()}"
    if (file.parents[-2] != output_folder):
        print("Working on " + input_file_path)
        Path(temp_output_file_path).parents[0].mkdir(parents=True, exist_ok=True)
        try:
            output_file_path = temp_output_file_path.replace(".docx", " - {word_count}.docx")
            # convertImage(input_file_path, output_file_path)
            word_count = 0
        except Exception:
            traceback.print_exc()
            print("    /!\ " + input_file_path + " failed /!\ \n")