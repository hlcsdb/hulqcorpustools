from pathlib import Path

from hulqcorpustools.transliterator import controller
from hulqcorpustools.resources.constants import TextFormat

from werkzeug.utils import secure_filename

def transliterate_string(
        hulq_string: str,
        source_format=(TextFormat | str),
        target_format=(TextFormat | str)
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
    print(hulq_string, source_format, target_format)
    return controller.string_transliterator(
        hulq_string,
        source_format,
        target_format)

def transliterate_file_list(
        file_list: list[Path | str],
        source_format=(TextFormat | str),
        target_format=(TextFormat | str),
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
 
    for _file in uploaded_files_list:
        _file.filename = secure_filename(_file.filename)

    ALLOWED_EXTENSIONS = {'.txt', '.docx', '.doc'}

    uploaded_files_list = [
        _file for _file in uploaded_files_list
        if Path(_file.filename).suffix in ALLOWED_EXTENSIONS
        ]

    UPLOADS_FOLDER = current_app.config['UPLOADS_FOLDER']
    upload_dir = Path(UPLOADS_FOLDER)

    uploaded_file_paths = []

    for i in uploaded_files_list:
        upload_path = Path(upload_dir.joinpath(i.filename))
        i.save(upload_path)
        uploaded_file_paths.append(upload_path)
    for file in file_list:
        print(file)

    file_controller = controller.TransliterandFileHandler(
        file_list,
        source_format=source_format,
        target_format=target_format,
        font=kwargs.get('font')
        )
    
    transliterated_files = file_controller.transliterated
    ...
    transliterated_files_dict = {
        i.name: str(i) for i in transliterated_files
    }
    
    return transliterated_files_dict