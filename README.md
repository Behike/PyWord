# PyWord

Parse DOC(X) files, (try to) format them with a uniform style and convert them to E-Pub format.

## Quickstart

Install all the required pip packages with, it's encourage to use a virtual environment first:
`pip install -r requirements.txt`

Create a folder called `0 - Input` (can be renamed in `Config/config.py`) and place all your DOCX/DOC files in it.

Edit `Config/config.py` if needed.

Execute `main.py`.

## Quick explanations

### main

Main functions to create the input/output folders, load each DOC(X) files in the input, and start each thread with each input file.

### html_parser

Functions to convert DOC(X) file to HTML, parse the result and format it.

### metada_parser

Functions to parse DOC(X) and HTML file to find all metada (EpubFileInfo class defined in this file) required to create an E-Pub file.

### epub_creator

Combine the formatted HTML string with the EpubFileInfo metadata to create an E-Pub file.

### config

Contains all settings used in the whole script, from Input/Output folder names to the font settings to be used while formatting.
