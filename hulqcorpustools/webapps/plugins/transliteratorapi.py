
from pathlib import Path

from flask import current_app, Request, g

from hulqcorpustools.transliterator.controller import (
    TransliterandFileHandler as tr_fh,
    string_transliterate as str_tr)
from hulqcorpustools.resources.constants import TextFormat
from hulqcorpustools.webapps.plugins import common

from werkzeug.datastructures import FileStorage, ImmutableMultiDict
from werkzeug.utils import secure_filename


def request_handler(
        request: Request,) -> tuple[dict, int]:
    source_format = TextFormat(request.form.get("source-format"))
    target_format = TextFormat(request.form.get("target-format"))
    if request.form.get("transliterate-input") == "string":
        response = transliterate_string(
            request.form.get("input-string"),
            source_format,
            target_format
        )

    elif request.form.get("transliterate-input") == "files":
        response = transliterate_file_list(
            request.files.getlist("files"),
            current_app.upload,
            source_format,
            target_format,
            font_search=request.form.get("font-search"),
        )
    else:
        response = ({"error": "request not understood"}, 400) 
    
    return response


def transliterate_string(
        string: str,
        source_format: TextFormat,
        target_format: TextFormat
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
    transliterated = str_tr(
        string,
        source_format,
        target_format
        )

    return ({
        "input_string": string,
        "source_format": source_format,
        "target_format": target_format,
        "output_string": transliterated},
        200)


def transliterate_file_list(
        file_list: list[FileStorage],
        upload: common.Upload,
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
    ALLOWED_EXTENSIONS = {'.txt', '.docx', '.doc'}

    file_list = [
        _file for _file in file_list
        if Path(_file.filename).suffix in ALLOWED_EXTENSIONS]

    for _file in file_list:
        _file.filename = secure_filename(_file.filename)

    file_controller = tr_fh(
        file_list,
        source_format=source_format,
        target_format=target_format,
        font=kwargs.get('font-search')
        )
    
    served_files = upload.save(file_controller.transliterated)
    
    if upload.upload_type != "s3":
        for _file in served_files:
            _file[1] = current_app.url_for(".download_file", file=_file[1])

    response = {"input_files": file_list,
                "source_format": str(source_format),
                "target_format": str(target_format),
                "output_files": served_files}

    return response, 200
