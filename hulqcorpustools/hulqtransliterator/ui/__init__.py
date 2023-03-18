

import importlib.resources
from pathlib import Path

from ..resources.constants import FileFormat
from ..transliterator import controller

def main(args=None):
    ...
    controller.FileController.docx_list_controller(docxfiles, source_format=FileFormat.ORTHOGRAPHY)

if __name__ == "__main__":
    main()