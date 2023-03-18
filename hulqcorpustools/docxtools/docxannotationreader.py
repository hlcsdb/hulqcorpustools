
from enum import Enum, EnumMeta
from importlib import resources
import os
from pathlib import Path
import re
from typing import Optional, Generator
from zipfile import BadZipFile

import docx

from ..resources import docxannotationdata


class HulqAnnotationStyles(Enum):

    annotation_template_docx = docx.Document(resources.open_binary(corpusdata,"hulq-story-annotation-template.docx"))

    annotation_names = [
    "Title",
    "Notes - Collection bibliographic notes",
    "Notes - Story bibliographic notes",
    "Text - Mention of Hul’q’umi’num’ word in Hul’q’umi’num’",
    "Notes - Story inline notes",
    "Notes",
    "Hul’q’umi’num’ line numbering",
    "Text line - Hul’q’umi’num’ line",
    "Text line - English translation of Hul’q’umi’num’",
    "Notes - Advice needed"
    "Text line - English spoken only",
    "Text - English word in Hul’q’umi’num’ line",
    "Text - Hul’q’umi’num’ word in English translation",
    "Text line - Hul’q’umi’num’ line with no translation",
    "Text - Speaker switch",
    "Story author name"]

    @classmethod
    def _get_hulq_annotation_styles(
        cls
    ):
        _docx_style_list = cls.annotation_template_docx.styles
        _annotation_styles = {
            _style.name : _style for _style in _docx_style_list
            if _style.name in cls.annotation_style_names
        }
        
        cls.hulq_annotation_styles = _annotation_styles
        return(_annotation_styles)


if __name__ == "__main__":
    corpus_docx_list = list(CorpusDocx(_corpus_docx) for _corpus_docx in Path(os.environ.get('CORPUS_TEST_DATA_FOLDER')).glob('*.docx'))
    