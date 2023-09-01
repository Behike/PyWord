from chapisha.create import CreateWork
from docx import Document
from config import *

docx_file = 'CHEATERS NOT SINNERS (EDITED) (1).docx'

document = Document(docx_file)

METADATA = {
    "identifier": "isbn:9780993191459",
    "title": str(document.core_properties.title),
    "description": str(document.core_properties.subject),
    "language": "en",
    "creator": [str(document.core_properties.author)],
    "rights": "All rights reserved.",
    "long_rights": ["The right of the creator to be identified as the author of the Work has been asserted by them in accordance with the Copyright, Designs and Patents Act 1988. This creator supports copyright. Copyright gives creators space to explore and provides for their long-term ability to sustain themselves from their work. Thank you for buying this work and for complying with copyright laws by not reproducing, scanning, or distributing any part of it without permission. Your support will contribute to future works by the creator."],
    "publisher": "Qwyre Publishing",
    "publisher_uri": "https://qwyre.com",
    "work-uri": "https://gavinchait.com",
    "date": "2017-07-23",
    "subject": ["science fiction", "african mythology"]
}

work = CreateWork('./')
# work = CreateWork(directory, metadata=metadata, stateless=True)

work.set_metadata(METADATA)