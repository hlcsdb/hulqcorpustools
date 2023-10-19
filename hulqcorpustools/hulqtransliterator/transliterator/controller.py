"""control room for the transliterator

from here, open files, get line, feed transliterator each line
 can deal with text files here for now, but docworker
will be the place to pull out lines from .docx

"""

from flashtext import KeywordProcessor
from pathlib import Path
import os
import shutil
import subprocess

import importlib.resources

from hulqcorpustools.resources.wordlists import wordlist_paths
from hulqcorpustools.utils.keywordprocessors import HulqKeywordProcessors
from hulqcorpustools.resources.constants import FileFormat, TransliterandFile, GraphemesDict
from hulqcorpustools.hulqtransliterator.filehandlers import docworker, txtworker
from . import replaceengine as repl

hulq_kp = HulqKeywordProcessors(eng=True)

class FileController():
    """Class that prepares the KeywordProcessors and transliterates the list of
    given files on demand.
    """
    def __init__(
            self,
            files_list = (list[Path]),
            source_format = (FileFormat | str | None),
            target_format = (FileFormat | str | None),
            **kwargs):
        """Prepare KeywordProcessors of the source format and target format 
        and hold lists of files for transliterating upon request.

        The reason docx files and txt files are both included in one controller
        is so as to not load multiple KeywordProcessors as it can take
        a few seconds each time it is initialized. The KPs can be loaded once
        to transliterate all desired files.

        
        Kwargsuments:
            docx_files -- a list of Paths to docx files to be transliterated
            txt_files: a list of Paths to txt files to be transliterated
            font  in the case of the font search, which font to search by
        """


        self.doc_files = list(filter(lambda x: x.suffix =='.doc', files_list)) # type: list[Path]
        self.docx_files = list(filter(lambda x: x.suffix == '.docx' and x.stem[0] != "~", files_list))
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

        self.source_format = source_format
        self.target_format = target_format
        self.search_method = kwargs.get('search_method')
        self.font_search = kwargs.get('font')

        if type(self.source_format) == str:
            self.source_format = FileFormat().from_string(self.source_format)

        if type(self.target_format) == str:
            self.source_format = FileFormat().from_string(self.target_format)

    def transliterate_all_files(
            self,
            **kwargs
        ):

        all_transliterated_files = []

        all_transliterated_files.extend(self.transliterate_docx_files(font=kwargs.get('font')))
        all_transliterated_files.extend(self.transliterate_txt_files())

        # transliterated_docx_files = self.transliterate_docx_files(font=kwargs.get('font')) 
        # transliterated_txt_files = self.transliterate_txt_files()

        return all_transliterated_files

    def transliterate_docx_files(
        self,
        **kwargs
        ):
        """manages the list of docx files

        Kwargs:
            update-wordlist: updates the Hul’q’umi’num’ wordlists with what gets found
        Returns:
            transliterated_files: a list of Paths the transliterated docx files
        """ 

        if kwargs.get('font') == True:
            transliterated_docx_files = [
                docworker.DocxTransliterator.transliterate_docx_font(
                    _file,
                    self.source_format,
                    self.target_format
                )
                for _file in self.docx_files
            ]
        else:
            source_kp = hulq_kp.get_kp(self.source_format)
            eng_kp = hulq_kp.eng_kp

            transliterated_docx_files = [
                docworker.DocxTransliterator.transliterate_docx_wordlist(
                    _file,
                    self.source_format,
                    self.target_format,
                    hulq_kp)
                    for _file in self.docx_files
                ]
            
        return transliterated_docx_files


    def transliterate_txt_files(
        self
        ):
        """transliterate a list of txt files
        """

        transliterated_txt_files = [
            txtworker.transliterate_txt_wordlist(
                _txt_file,
                self.source_format,
                self.target_format,
                hulq_kp.get_kp(self.source_format),
                hulq_kp.eng_kp
            )

            for _txt_file in self.txt_files
        ]
        return transliterated_txt_files

def string_processor(
    source_string: str,
    source_format: FileFormat,
    target_format: FileFormat):
    """just transliterates a single string.
    It's a thing of beauty"""

    transliterated_string = repl.transliterate_string_replace(
        source_string,
        source_format,
        target_format)
    return transliterated_string


if __name__ == "__main__":
    ...
    