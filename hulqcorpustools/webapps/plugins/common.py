
from io import BytesIO, TextIOWrapper
import mimetypes
import os
import time
from pathlib import Path
import shutil

import boto3
from werkzeug.utils import secure_filename
from werkzeug.wrappers.request import Request
from werkzeug.datastructures import FileStorage



ALLOWED_EXTENSIONS = {'.txt', '.docx', '.doc'}

class Upload():

    def __init__(
            self,
            upload_client,
            upload_bucket=None
    ):

        if isinstance(upload_client, Path):
            self.upload_type = "path"
            self.upload_path = upload_client
            self.save = self._hosted_save

        else:
            self.upload_type = "s3"
            self.client = upload_client  # Type: boto3.client
            self.bucket = upload_bucket
            self.save = self._s3_save

    def save(
            self,
            _files: list[Path]
        ):
        if self.upload_type == "s3":
            _save_method = self._s3_save
        elif self.upload_type == "path":
            _save_method = self._hosted_save

        saved_files = _save_method(_files)
        return(saved_files)


    def _s3_save(
            self,
            _files: list[Path]  # : Request.files
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
            self.client.upload_file(
                _file,
                self.bucket,
                _file.name
                # _file.filename
            )
            url = self.client.generate_presigned_url(
                "get_object", 
                Params={"Bucket": self.bucket,
                        "Key": _file.name},
                ExpiresIn=600)
            
            saved.append(
                {"filename": _file.name,
                 "url": url}
            )

        os.remove(_file)
        return saved

    def _hosted_save(
            self,
            _files: list[Path]
            ):

        saved_files = []
        for _file in _files:
            _out_path = self.upload_path.joinpath(_file.name)
            with open(_out_path, "wb") as out, open(_file, "rb") as f:
                ...
                out.write(f.read())

            saved_files.append(
                {"filename": _file.name,
                 "path": _out_path.relative_to(self.upload_path),
                 "url": _out_path
                }
            )
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

