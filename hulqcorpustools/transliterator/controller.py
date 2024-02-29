"""control room for the transliterator

from here, open files, get line, feed transliterator each line
 can deal with text files here for now, but docworker
will be the place to pull out lines from .docx

"""

from functools import partial
import os
from pathlib import Path

from werkzeug.datastructures import FileStorage
from docx import Document as load_docx
from docx.document import Document
from docx.text import paragraph

from hulqcorpustools.transliterator import replaceengine as repl
from hulqcorpustools.resources.constants import TextFormat
from hulqcorpustools.utils.files import FileHandler
from hulqcorpustools.utils.keywordprocessors import kp

class TransliterandFile():
    """_summary_
    """
    def __init__(
            self, 
            file: Path | str | FileStorage, 
            source_format: TextFormat, 
            target_format: TextFormat,
            **kwargs):

        if isinstance(file, (Path, str)):
            self.source_path = Path(file)
        elif isinstance(file, FileStorage):
            self.source_path = Path(file.filename)

        self.file = file
        self.name = self.source_path.name
        self.source_format = source_format
        self.target_format = target_format
        if (outdir := kwargs.get("outdir")):
            self.out_path = Path(outdir).joinpath(self.out_filename)

    @property
    def out_filename(self):
        return Path(
            f"{self.source_path.stem} - \
                {self.source_format} to {self.target_format}\
                {self.source_path.suffix}"
            )
    
    def __fspath__(self):
        return str(self.file)


class TransliterandFileHandler(FileHandler):
    """Class to hold all files to transliterate and transliterates them upon
    request.
    """
    def __init__(
            self,
            transliterand_files: list[TransliterandFile],
            **kwargs):

        self.transliterand_files = transliterand_files
        self.search_method = kwargs.get('search_method')
        if (source_format := kwargs.get("source_format")):
            for file in self.transliterand_files:
                file.source_format = source_formatA
        if (target_format := kwargs.get("target_format")):
            for file in self.transliterand_files:
                file.target_format = target_format
        super().__init__(self.transliterand_files)

        for i in args:
            print(i)

    @property
    def transliterated_docx(self):
        return [
            DocxTransliterator().transliterate(transliterand)
            for transliterand in self.docx_files
        ]
    
    @property
    def transliterated_txt(self):
        return [
            TxtTransliterator().transliterate(transliterand)
            for transliterand in self.txt_files
        ]

    @property
    def transliterated(self):
        return self.transliterate_all()

    def transliterate_all(self, **kwargs):

        all_transliterated_files = []
        all_transliterated_files.extend(
            self.transliterated_docx
            )
        all_transliterated_files.extend(
            self.transliterated_txt
            )

        return all_transliterated_files

    def transliterate_txt_files(
        self
        ):
        """transliterate a list of txt files
        """

        transliterated_txt_files = [
            # txt.transliterate_txt_wordlist(
            #     _txt_file,
            #     self.source_format,
            #     self.target_format,
            #     _kp.get_kp(self.source_format),
            #     _kp.eng_kp,
            #     outdir=self.out_dir
            # )

            # for _txt_file in self.txt_files
        ]
        return transliterated_txt_files


class DocxTransliterator():

    def _transliterate_paragraph_wordlist(
        self,
        par: paragraph,
        source_format: TextFormat,
        target_format: TextFormat,
        **kwargs):
        '''Transliterates an entire docx file by comparing to as wordlist

        Keyword arguments:
            update_wordlist -- include this if you want to update the wordlist
                            with words found in the transliterated lines
        '''
        new_par_text_parts = []
        # split at tab in case document separates English parts that way
        par_text_parts = par.text.split('\t')

        for par_text_part in par_text_parts:
            if kp.determine_language(par_text_part) != 'english':
                par_text_part = repl.transliterate_string(
                    par_text_part,
                    source_format,
                    target_format
                )
            new_par_text_parts.append(par_text_part)

            # reassemble tab-separated parts
            par.text = '\t'.join(new_par_text_parts)

    def _transliterate_paragraph_font(
        par: paragraph,
        target_format: TextFormat
        ):

        if par.style.font.name == 'Straight':
            par.text = repl.transliterate_string(
                par.text,
                TextFormat("straight"),
                target_format)

        else:
            for run in par.runs:
                if run.font.name == 'Straight':
                    run.text = repl.transliterate_string(
                        run.text,
                        TextFormat("straight"),
                        target_format
                    )

    def transliterate(
        self,
        transliterand: TransliterandFile,
        **kwargs
        ) -> Document:
        """delegate transliteration based on wordlist or font search

        Args:
            transliterand (TransliterandFile): _description_
            source_format (TextFormat): _description_
            target_format (TextFormat): _description_
        """
        
        document = load_docx(transliterand)
        if kwargs.get("search_format") == "font":
            _tr_fn = partial(
                self._transliterate_paragraph_font,
                target_format=transliterand.target_format
            )
        else:
            _tr_fn = partial(
                self._transliterate_paragraph_wordlist,
                source_format=transliterand.source_format,
                target_format=transliterand.target_format
            )

        for par in document.paragraphs:
            _tr_fn(par)

        for table in document.tables:
            for row in table.rows:
                for cell in row.cells:
                    for paragraph in cell.paragraphs:
                        _tr_fn(paragraph)

        return document

    # def update_new_wordlist(
    #     source_format: TextFormat,
    #     current_keywordprocessor: KeywordProcessor,
    #     new_keywords: list,
    #     keywordprocessors_dict: dict):
    #     """update the running wordlist with things that were transliterated

    #     Arguments:
    #         source_format -- the current source format (to get base wordlist folder)
    #         current_keywordprocessor -- the current keyword processor (to get the keywords)
    #         new_keywords -- all the found 
    #     """
    #     working_wordlist_filepath = Path(__file__).parent / ('resources/wordlists/new-hulq-wordlist-' +
    #                                                     source_format.to_string() +
    #                                                         '.txt')

    #     current_keywords = current_keywordprocessor.get_all_keywords()
        
    #     set(new_keywords.get_all_keywords().keys())


class TxtTransliterator():

    def transliterate_txt_wordlist(
        txt_transliterand: Path,
        source_format: TextFormat,
        target_format: TextFormat,
        **kwargs
        ):

        if kwargs.get('outdir'):
            out_dir = kwargs.get('outdir')
        else:
            out_dir = txt_transliterand.parent

        # out_filename = f"{txt_transliterand.stem}-{source_format}-to-{target_format}-transliterated.txt"
        # out_path = out_dir.joinpath(out_filename)
        # with (
        #     open(txt_transliterand, 'r+') as opened_source_file,
        #     open(out_path, 'w+') as opened_target_file
        # ):

        #     for line in opened_source_file:
        #         found_hulq_words = source_kp.extract_keywords(line)
        #         found_eng_words = eng_kp.extract_keywords(line)

        #     if len(found_hulq_words) > len(found_eng_words) or len(found_eng_words) == 0:
        #         transl_line = repl.transliterate_string(line, 
        #         source_format, 
        #         target_format)

        #         opened_target_file.write(line)

def string_transliterator(
    source_string: str,
    source_format: TextFormat,
    target_format: TextFormat
    ):
    """just transliterates a single string.
    It's a thing of beauty"""

    transliterated_string = repl.transliterate_string(
        source_string,
        source_format,
        target_format)
    return transliterated_string


if __name__ == "__main__":
    ...
    # cool = TransliterandFile(
    #     Path("tests/resources/docx/collection_numbered.docx"),
    #     TextFormat.ORTHOGRAPHY,
    #     TextFormat.APAUNICODE
    # )
    # great = TransliterandFile(
    #     Path("tests/resources/docx/collection_with_codes.docx"),
    #     TextFormat.ORTHOGRAPHY,
    #     TextFormat.APAUNICODE
    # )
    # awesome_file = FileStorage(
    #     open("tests/resources/docx/samuel_tom.docx")
    # ).filename
    # awesome = TransliterandFile(
    #     awesome_file,
    #     TextFormat.ORTHOGRAPHY,
    #     TextFormat.APAUNICODE)
    # my_files = TransliterandFileHandler([cool, great, awesome])

    # for i in my_files.transliterated:
    #     for j in i.paragraphs:
    #         print(j.text)
    # # for i in load_docx(cool.file).paragraphs:
    # #     print(i.text)

    # # tr_cool = DocxTransliterator().transliterate(cool)
    # # for i in tr_cool.paragraphs:
    # #     print(i.text)

    # ...
    