from docx import Document
from docx.shared import Pt, RGBColor
from docx.enum.style import WD_STYLE_TYPE
from docx.enum.text import WD_ALIGN_PARAGRAPH
from pathlib import Path
from re import compile, IGNORECASE
from config import *


def formatDocument(input, output):
    document = Document(input)

    author_name = document.core_properties.author
    created = document.core_properties.created
    created_year = "" if type(created) == type(None) else created.year

    ## Clean document
    # Remove empty paragraphs
    def delete_paragraph(paragraph):
        p = paragraph._element
        p.getparent().remove(p)
        p._p = p._element = None


    ### Format styles
    styles = document.styles

    ## Format title
    if ('Title' in document.styles):
        title_style = document.styles['Title']
    else:
        title_style = styles.add_style('Title', WD_STYLE_TYPE.PARAGRAPH)

    title_style.paragraph_format.alignment = title_paragraph_alignment
    title_style.paragraph_format.page_break_before = title_paragraph_page_break_before
    title_style.paragraph_format.space_before = title_paragraph_space_before
    title_style.paragraph_format.space_after = title_paragraph_space_after
    title_style.font.name = title_font_name
    title_style.font.size = title_font_size
    title_style.font.color.rgb = title_font_color

    ## Format chapters
    if ('Heading 1' in document.styles):
        heading_style = document.styles['Heading 1']
    else:
        heading_style = styles.add_style('Heading 1', WD_STYLE_TYPE.PARAGRAPH)

    heading_style.paragraph_format.alignment = heading_1_paragraph_alignment
    heading_style.paragraph_format.page_break_before = heading_1_paragraph_page_break_before
    heading_style.paragraph_format.space_before = heading_1_paragraph_space_before
    heading_style.paragraph_format.space_after = heading_1_paragraph_space_after
    heading_style.font.name = heading_1_font_name
    heading_style.font.size = heading_1_font_size
    heading_style.font.color.rgb = heading_1_font_color

    ## Format normal
    if ('Normal' in document.styles):
        normal_style = document.styles['Normal']
    else:
        normal_style = styles.add_style('Normal', WD_STYLE_TYPE.PARAGRAPH)

    normal_style.font.name = normal_font_name
    normal_style.font.size = normal_font_size

    ## Format subtitle
    if not ('Subtitle' in document.styles):
        subtitle_style = styles.add_style('Subtitle', WD_STYLE_TYPE.PARAGRAPH)
    else:
        subtitle_style = document.styles['Subtitle']
    
    subtitle_style.base_style = document.styles[subtitle_inherits_from]
    subtitle_style.paragraph_format.alignment = subtitle_paragraph_alignment
    subtitle_style.paragraph_format.space_after = subtitle_paragraph_space_after
    subtitle_style.font.name = subtitle_font_name
    subtitle_style.font.size = subtitle_font_size

    for para in document.paragraphs:
        para_text = para.text.strip()
        if (para_text != ""):        
            # Replace chapter name number in letter with the corresponding number
            if (any(map(para_text.upper().__contains__, chapter_dict.keys())) and len(para_text) <= CHAPTER_MAX_LENGTH):
                for substring in chapter_dict.keys():
                    if substring in para_text.upper():
                        chapter_found = substring
                if (chapter_found != ""):
                    pattern = compile(chapter_found, IGNORECASE)
                    para_text = pattern.sub(str(chapter_dict[chapter_found.upper()]), para_text)
                    para.text = para_text

            # Check for Heading 1 text (starting with header_1_names_list or numeric value and max 75 characters)
            if (((any(map(para_text.upper().__contains__, header_1_names_list)) or para_text[0].isnumeric()) and len(para_text) <= CHAPTER_MAX_LENGTH) or
                    (para.style.name == "Heading 1")):
                para.style = heading_style

            elif (para.style.name == "Title"):
                para.style = title_style
                # Add sub-title
                subtitle = document.add_paragraph(copyrightText(created_year, author_name), style='Subtitle')
                subt = subtitle._p
                p = para._p
                p.addnext(subt)

            else:
                para.style = normal_style
        else:
            delete_paragraph(para)
            
    # Save document
    document.save(output)



# Find all docx files in input folder and recreate subfolders in output_folder
files_list = list(Path().glob(input_folder + "/**/*.docx"))
for file in files_list:
    input_file_path = file.as_posix()
    output_file_path = output_folder + "/" + file.relative_to(*file.parts[:1]).as_posix()
    if (file.parents[-2] != output_folder):
        print("Working on " + input_file_path)
        Path(output_file_path).parents[0].mkdir(parents=True, exist_ok=True)
        # try:
        formatDocument(input_file_path, output_file_path)
        # except:
            # print("    /!\ " + input_file_path + " failed /!\ \n")
            
print("\n========== Finished ==========")
variable = input('Press anything to exit')