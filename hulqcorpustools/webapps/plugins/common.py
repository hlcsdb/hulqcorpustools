
from io import BytesIO, TextIOWrapper
import mimetypes
import os
from pathlib import Path

import boto3
from flask import current_app
from werkzeug.utils import secure_filename
from werkzeug.wrappers.request import Request
from werkzeug.datastructures import FileStorage

from hulqcorpustools.resources.constants import TextFormat

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


def save_filelist(
        _files: list[FileStorage],
):
    """Save files according to app config (either S3 bucket defined or locally hosted)

    Args:
        _files (list[FileStorage]): _description_
    """
    ...


def check_saveable():

    UPLOADS = current_app.config['UPLOADS']

    if UPLOADS == "s3" or Path(UPLOADS).exists():
        return True
    else:
        current_app.logger.error(
            "An upload location has not been properly configured. No file will be uploaded.")
        raise FileNotFoundError


def s3_save(
        _files: list[FileStorage]  # : Request.files
        ):
    """filter unacceptable filetypes, secure filenames, and save to secure path

    Args:
        _files: werkzeug Request.files
        _key: request key corresponding to form file submission (i.le. from html input.name)
        upload_dir: Path or str to where the files should be saved

    Returns:
        list of werkzeug.datastructures.FileStorage with filenames replaced with secure, full paths to where they are saved
    """
    saved_files = []
    for _file in _files:
        s3.upload_fileobj(
            _file,
            os.getenv("S3_BUCKET_NAME"),
            _file.filename
        )
        url = s3.generate_presigned_url(
            "get_object", 
            Params={"Bucket": os.getenv("S3_BUCKET_NAME"),
                    "Key": _file.filename},
            ExpiresIn=600)
        saved_files.append(
            (_file.filename, url)
        )
        _file.close()

    return saved_files


def hosted_save(_files: list[FileStorage]):
    upload_folder = Path(current_app.config.get("UPLOADS"))
    saved_files = []
    for _file in _files:
        _file_path = upload_folder.joinpath(_file.filename)
        _file.save(_file_path)

        saved_files.append((
            _file.filename, _file_path))
        _file.close()
    return saved_files