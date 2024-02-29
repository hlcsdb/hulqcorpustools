
import os
from pathlib import Path

import boto3
from werkzeug.utils import secure_filename
from werkzeug.wrappers.request import Request
from werkzeug.datastructures import FileStorage

# from hulqcorpustools.utils.keywordprocessors import kp

ALLOWED_EXTENSIONS = {'.txt', '.docx', '.doc'}

s3 = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("S3_BUCKET_ACCESS_KEY"),
    aws_secret_access_key=os.getenv("S3_BUCKET_SECRET_KEY"),
    endpoint_url=os.getenv("S3_DOMAIN"),
)


def secure_allowed_filelist(_filelist: Request.files):
    allowed_files = filter(allowed_file, _filelist)
    secured_files = map(secure_names, allowed_files)
    secured_files = list(secured_files)
    return secured_files


def allowed_file(_file: FileStorage):
    if Path(_file.filename).suffix in ALLOWED_EXTENSIONS:
        return True
    else:
        return False


def secure_names(_file: FileStorage):
    _file.filename = secure_filename(_file.filename)
    return _file


def save_safe_files(
        _files: Request.files,
        upload_dir: Path | str,
        ):
    """filter unacceptable filetypes, secure filenames, and save to secure path

    Args:
        _files: werkzeug Request.files
        _key: request key corresponding to form file submission (i.le. from html input.name)
        upload_dir: Path or str to where the files should be saved

    Returns:
        list of werkzeug.datastructures.FileStorage with filenames replaced with secure, full paths to where they are saved
    """
    secured_files = secure_allowed_filelist(_files)
    for _file in secured_files:
        s3.upload_fileobj(
            _file,
            os.getenv("S3_BUCKET_NAME"),
            _file.filename
        )


    return secured_files

