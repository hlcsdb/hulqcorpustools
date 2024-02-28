"""control room for the transliterator

from here, open files, get line, feed transliterator each line
 can deal with text files here for now, but docworker
will be the place to pull out lines from .docx

"""

from pathlib import Path

from werkzeug.datastructures import FileStorage

from hulqcorpustools.utils.files import FileHandler
from hulqcorpustools.utils.keywordprocessors import kp
from hulqcorpustools.resources.constants import TextFormat
from hulqcorpustools.hulqtransliterator.filehandlers import docworker, txtworker
from . import replaceengine as repl

class TransliterandFileHandler(FileHandler):
    """Class that prepares the KeywordProcessors and transliterates the list of
    given files on demand.
    """
    def __init__(
            self,
            files_list=(list[Path | FileStorage]),
            source_format=(TextFormat | str | None),
            target_format=(TextFormat | str | None),
            **kwargs):
        
        super().__init__(files_list)

        self.source_format = TextFormat(source_format)
        self.target_format = TextFormat(target_format)
        self.search_method = kwargs.get('search_method')
        self.font_search = kwargs.get('font')

    def transliterate_all_files(
            self,
            **kwargs
        ):

        all_transliterated_files = []

        all_transliterated_files.extend(self.transliterate_docx_files(
            font=kwargs.get('font')))
        all_transliterated_files.extend(self.transliterate_txt_files())

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

        if self.font_search == True:
            transliterated_docx_files = [
                docworker.DocxTransliterator.transliterate_docx_font(
                    _file,
                    self.source_format,
                    self.target_format,
                    outdir=self.out_dir
                )
                for _file in self.docx_files
            ]
        else:
            transliterated_docx_files = [
                docworker.DocxTransliterator.transliterate_docx_wordlist(
                    _file,
                    self.source_format,
                    self.target_format,
                    _kp,
                    outdir=self.out_dir)
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
                _kp.get_kp(self.source_format),
                _kp.eng_kp,
                outdir=self.out_dir
            )

            for _txt_file in self.txt_files
        ]
        return transliterated_txt_files

def string_transliterator(
    source_string: str,
    source_format: TextFormat,
    target_format: TextFormat
    ):
    """just transliterates a single string.
    It's a thing of beauty"""

    transliterated_string = repl.transliterate_string_replace(
        source_string,
        source_format,
        target_format)
    return transliterated_string


if __name__ == "__main__":
    ...
    