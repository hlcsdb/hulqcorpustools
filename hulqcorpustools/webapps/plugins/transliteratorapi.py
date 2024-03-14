
from pathlib import Path
import time

from flask import current_app, Request, g

from hulqcorpustools.resources.constants import TextFormat
from hulqcorpustools.webapps.plugins import common
from hulqcorpustools.transliterator.controller import (
    Transliterator as transl,
    TransliterandFileHandler as transl_fh)

from werkzeug.datastructures import FileStorage, ImmutableMultiDict
from werkzeug.utils import secure_filename


def request_handler(
        request: Request,) -> tuple[dict, int]:
    source_format = TextFormat(request.form.get("source-format"))
    target_format = TextFormat(request.form.get("target-format"))

    tr = current_app.transliterator  # type: transl
    tmp = current_app.config.get("TMP")
    if request.form.get("transliterate-input") == "string":
        response = tr_string_request(
            request.form.get("input-string"),
            source_format,
            target_format,
            tr
        )

    elif request.form.get("transliterate-input") == "files":
        response = tr_file_list_request(
            request.files.getlist("files"),
            current_app.upload,
            tr,
            source_format,
            target_format,
            font_search=request.form.get("font-search"),
            tmp=tmp
        )
    else:
        response = ({"error": "request not understood"}, 400) 
    
    return response


def tr_string_request(
        string: str,
        source_format: TextFormat,
        target_format: TextFormat,
        tr: transl
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
    transliterated = tr.transliterate_string(
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


def tr_file_list_request(
        file_list: list[FileStorage],
        upload: common.Upload,
        _tr: transl,
        source_format=(TextFormat | str),
        target_format=(TextFormat | str),
        tmp=Path,
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

    # time.sleep(5)
    file_list = [
        _file for _file in file_list
        if Path(_file.filename).suffix in ALLOWED_EXTENSIONS]

    for _file in file_list:
        _file.filename = secure_filename(_file.filename)
        _file_path = Path(tmp / _file.filename)
        _file.save(_file_path)
        _file = _file_path

    # time.sleep(5)
    file_handler = transl_fh(
        file_list,
        _tr,
        source_format=source_format,
        target_format=target_format,
        font=kwargs.get('font-search'),
        out=tmp
        )
    
    # time.sleep(5)
    transliterated = file_handler.transliterated()

    # time.sleep(5)
    served_files = upload.save(transliterated)
    
    if upload.upload_type != "s3":
        for _file in served_files:
            _file["url"] = current_app.url_for(
                ".download_file",
                file=_file,
                filename=_file["path"])

    response = {"input_files": file_list,
                "source_format": str(source_format),
                "target_format": str(target_format),
                "output_files": served_files}

    # time.sleep(5)
    return response, 200
