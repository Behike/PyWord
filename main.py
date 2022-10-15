from docx import Document
from datetime import datetime
from docx.shared import Inches, Pt, RGBColor
from docx.enum.style import WD_STYLE_TYPE
from docx.enum.text import WD_ALIGN_PARAGRAPH
from pathlib import Path
import time

input_folder = "0 - Input"
output_folder = "0 - Output"


def formatDocument(input, output):
    document = Document(input)

    author = document.core_properties.author
    created = document.core_properties.created
    created_year = "" if type(created) == type(None) else created.year

    copyright_text = "Copyright © " + str(created_year) + " " + author + "\nAll rights reserved. No parts of this publication may be reproduced, \
    stored in a retrieval system, or transmitted in any form or by any means, electronic, mechanical, photocopying, \
    recording, or otherwise, without the prior written permission of the copyright owner.\nThis book is sold subject \
    to the condition that it shall not, by way of trade or otherwise, be lent, resold, hired out, or otherwise circulated \
    without the publisher’s prior consent in any form of binding or cover other than that in which it is published and \
    without a similar condition including this condition being imposed on the subsequent purchaser. Under no circumstances \
    may any part of this book be photocopied for resale.\nThis is a work of fiction. Any similarity between the characters \
    and situations within its pages and places or persons, living or dead, is unintentional and co-incidental."

    ## Clean document
    # Remove empty paragraphs
    def delete_paragraph(paragraph):
        p = paragraph._element
        p.getparent().remove(p)
        p._p = p._element = None


    ### Format styles
    styles = document.styles

    ## Format title
    # if not ('TitleCustom' in document.styles):
    #     title_style = styles.add_style('TitleCustom', WD_STYLE_TYPE.PARAGRAPH)
    # else:
    #     title_style = document.styles['TitleCustom']

    if ('Title' in document.styles):
        # title_style.base_style = document.styles['Title']
        title_style = document.styles['Title']
    else:
        title_style = styles.add_style('Title', WD_STYLE_TYPE.PARAGRAPH)

    title_style.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    title_style.paragraph_format.page_break_before = True
    title_style.paragraph_format.space_before = Pt(45)
    title_style.paragraph_format.space_after = Pt(45)
    title_style.font.name = "Cambria"
    title_style.font.size = Pt(36)
    title_style.font.color.rgb = RGBColor(0x0,0x0,0x0)

    ## Format chapters
    # if not ('Chapter' in document.styles):
    #     heading_style = styles.add_style('Chapter', WD_STYLE_TYPE.PARAGRAPH)
    # else:
    #     heading_style = document.styles['Chapter']

    if ('Heading 1' in document.styles):
        # heading_style.base_style = document.styles['Heading 1']
        heading_style = document.styles['Heading 1']
    else:
        heading_style = styles.add_style('Heading 1', WD_STYLE_TYPE.PARAGRAPH)

    heading_style.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    heading_style.paragraph_format.page_break_before = True
    heading_style.paragraph_format.space_before = Pt(45)
    heading_style.paragraph_format.space_after = Pt(45)
    heading_style.font.name = "Palatino Linotype"
    heading_style.font.size = Pt(36)
    heading_style.font.color.rgb = RGBColor(0x0,0x0,0x0)

    for val in document.styles['Heading 1']:
        print(val + " - " + heading_style.val)

    ## Format normal
    # if not ('NormalCustom' in document.styles):
    #     normal_style = styles.add_style('NormalCustom', WD_STYLE_TYPE.PARAGRAPH)
    # else:
    #     normal_style = document.styles['NormalCustom']

    if ('Normal' in document.styles):
        # normal_style.base_style = document.styles['Normal']
        normal_style = document.styles['Normal']
    else:
        normal_style = styles.add_style('Normal', WD_STYLE_TYPE.PARAGRAPH)

    normal_style.font.name = "Palatino Linotype"
    normal_style.font.size = Pt(10)

    ## Format subtitle
    # if not ('SubtitleCustom' in document.styles):
    #     subtitle_style = styles.add_style('SubtitleCustom', WD_STYLE_TYPE.PARAGRAPH)
    # else:
    #     subtitle_style = document.styles['SubtitleCustom']

    if not ('Subtitle' in document.styles):
        subtitle_style = styles.add_style('Subtitle', WD_STYLE_TYPE.PARAGRAPH)
    else:
        subtitle_style = document.styles['Subtitle']
    # if ('Normal' in document.styles):
        # subtitle_style.base_style = document.styles['Normal']
    subtitle_style.base_style = document.styles['Normal']
    subtitle_style.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    subtitle_style.paragraph_format.space_after = Pt(45)
    subtitle_style.font.name = "Palatino Linotype"
    subtitle_style.font.size = Pt(9)

    for para in document.paragraphs:
        if (para.text == ""):
            delete_paragraph(para)

        elif ((para.text[:7] == "Chapter") or
                (para.text[:8] == "Prologue") or
                (para.text[:8] == "Epilogue") or
                (para.style.name == "Heading 1") or
                (para.text[0].isnumeric() and (len(para.text) <= 75))):
            para.style = heading_style

        elif (para.style.name == "Title"):
            para.style = title_style
            # Add sub-title
            # subtitle = document.add_paragraph(copyright_text, style='SubtitleCustom')
            subtitle = document.add_paragraph(copyright_text, style='Subtitle')
            subt = subtitle._p
            p = para._p
            p.addnext(subt)

        else:
            para.style = normal_style
            # para.style.font.name = "Palatino Linotype"
            # normal_style.font.size = Pt(10)
            
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