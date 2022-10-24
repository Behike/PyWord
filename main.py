from docx import Document
from docx.shared import Pt, RGBColor
from docx.enum.style import WD_STYLE_TYPE
from docx.enum.text import WD_ALIGN_PARAGRAPH
from pathlib import Path
from re import compile, search, escape, findall, IGNORECASE
from config import *
import traceback

word_count = 0

def formatDocument(input, output):
    global word_count
    title_added = False

    document = Document(input)

    author_name = document.core_properties.author
    created = document.core_properties.created
    created_year = "" if type(created) == type(None) else created.year

    ## Clean document
    # Remove empty paragraphs
    def deleteParagraph(paragraph):
        p = paragraph._element
        p.getparent().remove(p)
        p._p = p._element = None

    # Add subtitle after title
    def addSubtitle(para):
        subtitle = document.add_paragraph(copyrightText(created_year, author_name), style='Subtitle')
        subt = subtitle._p
        p = para._p
        p.addnext(subt)

    ### Format styles
    styles = document.styles

    ## Format title
    if ('Title' in document.styles):
        document.styles['Title'].delete()

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
        document.styles['Heading 1'].delete()

    heading_style = styles.add_style('Heading 1', WD_STYLE_TYPE.PARAGRAPH)

    heading_style.paragraph_format.alignment = heading_1_paragraph_alignment
    heading_style.paragraph_format.page_break_before = heading_1_paragraph_page_break_before
    heading_style.paragraph_format.space_before = heading_1_paragraph_space_before
    heading_style.paragraph_format.space_after = heading_1_paragraph_space_after
    heading_style.font.name = heading_1_font_name
    heading_style.font.size = heading_1_font_size
    heading_style.font.color.rgb = heading_1_font_color

    ## Format normal
    if ('NormalCustom' in document.styles):
        document.styles['NormalCustom'].delete()
    
    normal_style = styles.add_style('NormalCustom', WD_STYLE_TYPE.PARAGRAPH)

    normal_style.paragraph_format.first_line_indent = normal_paragraph_first_line_indent
    normal_style.paragraph_format.left_indent = normal_paragraph_left_indent
    normal_style.paragraph_format.right_indent = normal_paragraph_right_indent
    normal_style.paragraph_format.alignment = normal_paragraph_alignment
    normal_style.paragraph_format.space_before = normal_paragraph_space_before
    normal_style.paragraph_format.space_after = normal_paragraph_space_after
    normal_style.paragraph_format.page_break_before = normal_paragraph_page_break_before
    normal_style.font.name = normal_font_name
    normal_style.font.size = normal_font_size
    normal_style.font.color.rgb = normal_font_color

    ## Format subtitle
    if ('Subtitle' in document.styles):
        document.styles['Subtitle'].delete()

    subtitle_style = styles.add_style('Subtitle', WD_STYLE_TYPE.PARAGRAPH)
    
    subtitle_style.base_style = document.styles[subtitle_inherits_from]
    subtitle_style.paragraph_format.alignment = subtitle_paragraph_alignment
    subtitle_style.paragraph_format.space_after = subtitle_paragraph_space_after
    subtitle_style.font.name = subtitle_font_name
    subtitle_style.font.size = subtitle_font_size

    for para in document.paragraphs:
        para_text = para.text.strip()

        para.paragraph_format.first_line_indent = None
        para.paragraph_format.left_indent = None
        para.paragraph_format.right_indent = None

        if (para_text != ""):
            if (para.style.name == "Title" and not title_added):
                para.style = title_style
                addSubtitle(para)
                title_added = True

            # Check for Heading 1 text (starting with header_1_names_list or numeric value and max 75 characters)
            elif ((len(para_text) <= CHAPTER_MAX_LENGTH) or (para.style.name == heading_style.name)):
                # List of header 1 keywords present at the beginning of the text (empty or one word only)
                header_1_keyword_first = [ele for ele in header_1_names_list if para_text.upper().startswith(ele)]
                # List of digits in text
                digit = [ele for ele in para_text if ele.isdigit()]
                # List of letter numbers (whole word only)
                # re.search(r"\b" + re.escape(ele) + r"\b", para_text.upper())
                letter_number = [ele for ele in number_dict.keys() if search(r"\b" + escape(ele) + r"\b", para_text.upper())]

                # If whole text is a number
                if (para_text.isdigit()):
                    para.style = heading_style

                # If whole text is a number (in letter) convert it to number
                if (letter_number and para_text == letter_number[0]):
                    para_text = str(number_dict[letter_number[0]])
                    para.style = heading_style

                # Replace chapter name number in letter with the corresponding number
                elif (header_1_keyword_first):
                    # if (any(map(para_text.upper().__contains__, number_dict.keys()))):
                    if (letter_number):
                        for substring in number_dict.keys():
                            if substring in para_text.upper():
                                chapter_number_found = substring
                        if (chapter_number_found != ""):
                            pattern = compile(chapter_number_found, IGNORECASE)
                            para_text = pattern.sub(str(number_dict[chapter_number_found.upper()]), para_text)
                        
                    if (len(para_text.split()) >= 2 and para_text.split()[1].isdigit()):
                        para_text = para_text[len(header_1_keyword_first[0])+1:]

                    para.style = heading_style

                # If no conditions were met, apply normal style
                if (para.style != heading_style):
                    para.style = normal_style

            else:
                para.style = normal_style
            
            para.text = para_text

        else:
            deleteParagraph(para)

        # word_count = word_count + len(findall(r'\w+', para_text))
        word_count = word_count + len(para_text.split())
            
    for section in document.sections:
        if (section.header):
            section.header.is_linked_to_previous = True
        if (section.footer):
            section.footer.is_linked_to_previous = True

    if (document.paragraphs and not title_added):
        document.paragraphs[0].insert_paragraph_before(file.name.replace(".docx", ""), style='Title')
        addSubtitle(document.paragraphs[0])
        title_added = True

    # Save document
    document.save(output.format(word_count=word_count))


# Find all docx files in input folder and recreate subfolders in output_folder
files_list = list(Path().glob(input_folder + "/**/*.docx"))
for file in files_list:
    input_file_path = file.as_posix()
    temp_output_file_path = f"{output_folder}/{file.relative_to(*file.parts[:1]).as_posix()}"
    if (file.parents[-2] != output_folder):
        print("Working on " + input_file_path)
        Path(temp_output_file_path).parents[0].mkdir(parents=True, exist_ok=True)
        try:
            output_file_path = temp_output_file_path.replace(".docx", " - {word_count}.docx")
            formatDocument(input_file_path, output_file_path)
            word_count = 0
        except Exception:
            traceback.print_exc()
            print("    /!\ " + input_file_path + " failed /!\ \n")

print("\n========== Finished ==========")
variable = input('Press enter to exit')