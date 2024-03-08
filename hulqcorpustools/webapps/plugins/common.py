
from io import BytesIO, TextIOWrapper
import mimetypes
import os
from pathlib import Path

import boto3
from werkzeug.utils import secure_filename
from werkzeug.wrappers.request import Request
from werkzeug.datastructures import FileStorage

from hulqcorpustools.resources.constants import TextFormat

ALLOWED_EXTENSIONS = {'.txt', '.docx', '.doc'}

class Upload():

    def __init__(
            self,
            upload_client,
            upload_bucket=None
    ):

        if isinstance(upload_client, Path):
            self.upload_type = "path"
            self.save = self._hosted_save

        else:
            self.upload_type = "s3"
            self.client = upload_client  # Type: boto3.client
            self.bucket = upload_bucket
            self.save = self._s3_save

    def _s3_save(
            self,
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

        saved = []
        for _file in _files:
            self.client.upload_fileobj(
                _file,
                self.bucket,
                _file.filename
            )
            url = self.client.generate_presigned_url(
                "get_object", 
                Params={"Bucket": self.bucket,
                        "Key": _file.filename},
                ExpiresIn=600)
            
            saved.append(
                (_file.filename, url)
            )
            _file.close()

        return saved

    def _hosted_save(
            _upload: Path,
            _files: list[FileStorage]
            ):

        saved_files = []
        for _file in _files:
            _file_path = _upload.joinpath(_file.filename)
            _file.save(_file_path)

            saved_files.append((
                _file.filename, _file_path))
            _file.close()
        return saved_files
    

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
