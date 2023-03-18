
from pathlib import Path
from typing import Optional, Generator, Iterable

import docx

from ..utils import plaintext

def docx_text_extract(
    docx_file: Path
    ) -> Generator:

    _docx_document = docx.Document(docx_file)
    for paragraph in _docx_document.paragraphs:
        yield paragraph.text + '\n'