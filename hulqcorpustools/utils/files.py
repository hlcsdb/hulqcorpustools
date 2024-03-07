
from io import BytesIO
from functools import partial
from pathlib import Path
import mimetypes
import shutil
import subprocess

from werkzeug.datastructures import FileStorage


class FileHandler():
    """Class for dealing with lists of files which have been saved to the
    filesystem and are accessible by Path.
    """
    def __init__(
            self,
            files_list=list[Path | str | FileStorage],
            **kwargs):

        self.files_list = files_list
        self.docx_files = list(filter(
            partial(self.filter_suffix, ".docx"), self.files))  # type: list[FileStorage]
        self.txt_files = list(filter(
            partial(self.filter_suffix, ".txt"), self.files))  # type: list[FileStorage]
        self.doc_files = list(filter(
            partial(self.filter_suffix, ".doc"), self.files))  # type: list[FileStorage]

        if self.doc_files:
            map(self.convert_doc, filter(
                partial(self.filter_suffix, ".doc"), self.files
            ))

        self.out_dir = kwargs.get('outdir')
        self.tmp_dir = kwargs.get('tmpdir')

    @property
    def files(self):
        _files = []
        for _file in self.files_list:
            if isinstance(_file, Path | str):
                _file = FileStorage(
                    BytesIO(open(_file, "rb")),
                    Path(_file))

            _files.append(_file)

        return _files


    def filter_suffix(self, key_suffix: str, file: FileStorage):
        _suffix = Path(file.filename).suffix
        if _suffix == key_suffix:
            return True

    def convert_doc(self, doc_file: FileStorage):
        if not shutil.which('soffice'):
            print('libreoffice not installed! Skipping .doc files...')
            return

        soffice_convert_cmd = [
            'soffice', '--headless', '--convert-to', 'docx'
            ]
        if self.tmp_dir:
            _doc_convert_tmpdir = self.tmp_dir
        else:
            _doc_convert_tmpdir = self.doc_files[0].parent

        # construct command
        soffice_convert_cmd.extend([
            '--outdir', _doc_convert_tmpdir, str(doc_file.key)
            ])
        subprocess.run(soffice_convert_cmd)

        converted_docx_path = _doc_convert_tmpdir.joinpath(
            Path(doc_file.key).with_suffix(".docx"))
        converted = FileStorage(
            BytesIO(open(converted_docx_path, "rb")),
            converted_docx_path,
            mimetypes.types_map[".docx"])
        
        self.docx_files.extend(converted)
