
from pathlib import Path
import shutil
import subprocess

from werkzeug.datastructures import FileStorage


class FileHandler():
    """Class for dealing with lists of files which have been saved to the
    filesystem and are accessible by Path.
    """
    def __init__(
            self,
            files_list=(list[Path | str | FileStorage]),
            **kwargs):
        """

        Args:
            files_list (tuple, optional): _description_. Defaults to (list[Path  |  str]).

        Kwargs:
            outdir (Path, optional): For file-saving operations (e.g. transliteration),
            where to save those files.
            tmpdir (Path, optional): When a temporary directory is needed, e.g.
            for temporarily saving .doc files to convert, where that temporary
            directory should be.
        """
        
        self.doc_files = list(filter(
            lambda x: Path(x).suffix == '.doc', files_list
            ))
        self.docx_files = list(filter(
            lambda x: Path(x).suffix == '.docx' and Path(x).stem[0] != "~", files_list
            ))  # type: list[Path]
        self.txt_files = list(filter(
            lambda x: Path(x).suffix == '.txt', files_list
            ))

        self.out_dir = kwargs.get('outdir')
        self.tmp_dir = kwargs.get('tmpdir')

        if self.doc_files:
            self.convert_doc_files()

    def convert_doc_files(self):
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
            '--outdir', _doc_convert_tmpdir
            ])
        soffice_convert_cmd.extend((
            str(_doc_file) for _doc_file in self.doc_files
            ))
        subprocess.run(soffice_convert_cmd)

        _new_docx_files = [
            _doc_convert_tmpdir.joinpath(
                _doc_file.with_suffix('.docx')) for _doc_file in self.doc_files
            ]

        # add converted .doc to list of .docx
        self.docx_files.extend(_new_docx_files)
        return
