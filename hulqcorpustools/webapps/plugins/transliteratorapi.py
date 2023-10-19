from pathlib import Path

from hulqcorpustools.hulqtransliterator.transliterator import controller
from hulqcorpustools.resources.constants import FileFormat

def transliterate_string(
        hulq_string: str,
        source_format = (FileFormat | str),
        target_format = (FileFormat | str)
        ) -> str:
    """Transliterate a single string to return to the webpage.

    Arguments:
        hulq_string -- a single string of Hul’q’umi’num’

    Keyword Arguments:
        source_format -- the format of the initial string (default: {(FileFormat  |  str)})
        target_format -- the format to be transliterated into (default: {(FileFormat  |  str)})

    Returns:
        A single transliterated string.
    """
    if type(source_format) == str:
        source_format = FileFormat.from_string(source_format)
        
    if type(target_format) == str:
        target_format = FileFormat.from_string(target_format)
    
    return controller.string_processor(hulq_string, source_format, target_format)

def transliterate_file_list(
        file_list: list[Path | str],
        source_format = (FileFormat | str),
        target_format = (FileFormat | str),
        **kwargs) -> dict[str: list[Path]]:
    """Transliterate multiple files that have been uploaded.
    The file is transliterated and saved in the same directory it exists in.

    Arguments:
        file_list -- a Path (or str of a path) to a file.
        source_format -- the format of the initial text to be transliterated
            (default: {(FileFormat  |  str)})
        target_format -- the format to be transliterated into
            (default: {(FileFormat  |  str)})

    Returns:
        A dict with entries 'transliterated_docx', 'transliterated_txt'
        corresponding each to a list of paths to the newly transliterated files

    """
    

    if type(source_format) == str:
        source_format = FileFormat.from_string(source_format)

    if type(target_format) == str:
        target_format = FileFormat.from_string(target_format)

    file_controller = controller.FileController(
        file_list,
        source_format=source_format,
        target_format=target_format,
        font=kwargs.get('font')
        )
    
    transliterated_files = file_controller.transliterate_all_files()
    ...
    transliterated_files_dict = {
        i.name : str(i)  for i in transliterated_files
    }

    # transliterated_txt_files = {
    #     i.name : str(i) for i in file_controller.transliterate_txt_files()
    # }
    
    return transliterated_files_dict