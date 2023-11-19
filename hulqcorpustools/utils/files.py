
from pathlib import Path
import shutil
import subprocess

class FileHandler():

    def __init__(
            self,
            files_list = (list[Path | str]),
            **kwargs):

        self.doc_files = list(filter(lambda x: x.suffix =='.doc', files_list)) 
        self.docx_files = list(filter(lambda x: x.suffix == '.docx' and x.stem[0] != "~", files_list)) # type: list[Path]
        self.txt_files = list(filter(lambda x: x.suffix == '.txt', files_list))
        self.out_dir = kwargs.get('outdir')
        self.tmp_dir = kwargs.get('tmpdir')

        if self.doc_files != []:
            if shutil.which('soffice'):
                soffice_convert_cmd = ['soffice', '--headless', '--convert-to', 'docx']
                
                
                if self.tmp_dir:
                    _doc_convert_tmpdir = self.tmp_dir
                # use first file location if none provided
                else:
                    _doc_convert_tmpdir = self.doc_files[0].parent
                soffice_convert_cmd.extend(['--outdir', _doc_convert_tmpdir])
                soffice_convert_cmd.extend((str(_doc_file) for _doc_file in self.doc_files))
                subprocess.run(soffice_convert_cmd)
                _new_docx_files = [_doc_convert_tmpdir.joinpath(_doc_file.with_suffix('.docx')) for _doc_file in self.doc_files]

                self.docx_files.extend(_new_docx_files)
            else:
                print('libreoffice not installed! Skipping .doc files...')
