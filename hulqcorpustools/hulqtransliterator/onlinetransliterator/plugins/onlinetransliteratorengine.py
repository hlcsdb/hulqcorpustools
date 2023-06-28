from pathlib import Path

from hulqcorpustools.hulqtransliterator.transliterator import controller
from hulqcorpustools.resources.constants import FileFormat

def _transliterate_string(hulq_string: str,
                            source_format = (FileFormat | str),
                            target_format = (FileFormat | str)):

    if type(source_format) == str:
        source_format = FileFormat.from_string(source_format)
        
    if type(target_format) == str:
        target_format = FileFormat.from_string(target_format)
    
    return controller.string_processor(hulq_string, source_format, target_format)

def _transliterate_file(
        file: (Path | str),
        source_format = FileFormat | str,
        target_format = FileFormat | str):
    
    if type(file) == str:
        file = Path(file)

    if type(source_format) == str:
        source_format = FileFormat.from_string(source_format)

    if type(target_format) == str:
        target_format = FileFormat.from_string(target_format)

    docx_file_list = []
    txt_file_list = []

    if file.suffix[1:] == 'docx':
        docx_file_list.append(file)

    elif file.suffix[1:] == 'txt':
        txt_file_list.append(file)

    file_controller = controller.FileController(
        docx_file_list,
        txt_file_list,
        source_format=source_format,
        target_format=target_format)
    
    transliterated_docx_files = {
        i.name : str(i)  for i in file_controller.transliterate_docx()
    }
    transliterated_txt_files = {
        i.name : str(i) for i in file_controller.transliterate_txt()
    }
    
    transliterated_files = {
        'transliterated_docx': transliterated_docx_files,
        'transliterated_txt': transliterated_txt_files
        }
    return transliterated_files