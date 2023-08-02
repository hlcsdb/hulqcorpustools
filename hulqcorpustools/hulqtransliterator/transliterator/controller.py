"""control room for the transliterator

from here, open files, get line, feed transliterator each line
 can deal with text files here for now, but docworker
will be the place to pull out lines from .docx

"""

from flashtext import KeywordProcessor
from pathlib import Path
import os

import importlib.resources

from hulqcorpustools.resources.wordlists import wordlist_paths
from hulqcorpustools.utils.keywordprocessors import HulqKeywordProcessors
from hulqcorpustools.resources.constants import FileFormat, TransliterandFile, GraphemesDict
from hulqcorpustools.hulqtransliterator.filehandlers import docworker, txtworker
from . import replaceengine as repl

# TODO: use keyword processors in utils

_hulqkp = HulqKeywordProcessors(eng=True)

class FileController():
    """Class that prepares the KeywordProcessors and transliterates the list of
    given files on demand.
    """
    def __init__(
            self,
            docx_files = (list[Path] | None),
            txt_files = (list[Path] | None),
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
        self.docx_files = docx_files
        self.txt_files = txt_files
        self.source_format = source_format

        self.target_format = target_format
        
        self.search_method = kwargs.get('search_method')
        self.font_search = kwargs.get('font')

        if type(self.source_format) == str:
            self.source_format = FileFormat().from_string(self.source_format)

        if type(self.target_format) == str:
            self.source_format = FileFormat().from_string(self.target_format)


    def transliterate_docx(
        self
        ):
        """manages the list of docx files

        Kwargs:
            update-wordlist: updates the Hul’q’umi’num’ wordlists with what gets found
        Returns:
            transliterated_files: a list of Paths the transliterated docx files
        """ 

        if self.docx_files is None:
            return []

        transliterated_docx_files = []

        source_kp = _hulqkp.get_kp(self.source_format)
        eng_kp = _hulqkp.eng_kp

        for i in self.docx_files:
            docx_transliterand = TransliterandFile(
                i,
                self.source_format,
                self.target_format
                )

            transliterated_docx_files.append(
                docworker.transliterate_docx_wordlist(
                docx_transliterand,
                source_kp,
                eng_kp))

        return transliterated_docx_files

    def transliterate_txt(
        self
        ):
        """transliterate a list of txt files
        """
        if self.txt_files is None:
            return []

        transliterated_txt_files = []

        for i in self.txt_files:
            txt_transliterand = TransliterandFile(
                i,
                self.source_format,
                self.target_format
                )
            
            source_kp = _hulqkp.get_kp(self.source_format)
            eng_kp = _hulqkp.eng_kp

            transliterated_txt_files.append(
                txtworker.transliterate_txt_wordlist(
                txt_transliterand,
                source_kp,
                eng_kp
                )
                )

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

# def collect_keywordprocessors(*file_formats):
    
#     collected_kps = dict()
#     english_keywordprocessor = prepare_engkeywordprocessor()
#     collected_kps.update({"english": english_keywordprocessor})
#     for i in file_formats:
#         hulq_keywordprocessor = prepare_hulqkeywordprocessor(i)
#         collected_kps.update({i.to_string(): hulq_keywordprocessor})

#     return collected_kps
    
# def prepare_engkeywordprocessor():
#     eng_wordlist_filepath = wordlist_paths.get("words_alpha_vowels_longer_words")

#     eng_keywordprocessor = KeywordProcessor()
#     eng_keywordprocessor.add_keyword_from_file(eng_wordlist_filepath)

#     return eng_keywordprocessor

# def prepare_hulqkeywordprocessor(file_format: FileFormat, **kwargs) -> dict:
#     """opens up wordlists for transliteration

#     Arguments:
#         source_format -- the source format to be transliterated
#     Kwargs:
#         --update-wordlist: opens the other format wordlists if they are supposed to be
#         updated
#     """

#     def get_non_word_boundary_chars(text_format: FileFormat):
#         """gets all of the characters that might not be in [a-zA-Z] or whatever

#         Arguments:
#             text_format -- a FileFormat of some source
#         """
#         non_word_boundary_chars = (i for i in GraphemesDict(text_format).source_format_characters)
#         return non_word_boundary_chars

#     file_format_name = file_format.to_string()
#     hulq_wordlist_filename = f'hulq-wordlist-{file_format_name}'
#     hulq_wordlist_filepath = wordlist_paths.get(hulq_wordlist_filename)

#     hulq_keywordprocessor = KeywordProcessor()
#     hulq_keywordprocessor.set_non_word_boundaries(get_non_word_boundary_chars(file_format))
#     hulq_keywordprocessor.add_keyword_from_file(hulq_wordlist_filepath)

#     return hulq_keywordprocessor


if __name__ == "__main__":
    ...
    