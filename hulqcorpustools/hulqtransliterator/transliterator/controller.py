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
from hulqcorpustools.resources.constants import FileFormat, TransliterandFile, GraphemesDict
from hulqcorpustools.hulqtransliterator.filehandlers import docworker, txtworker
from . import replaceengine as repl

# TODO: add feature to transliterate *only* hulq words
# may take a much more substantial wordlist

class FileController():
    
    def __init__(
            self,
            docx_files = (list | None),
            txt_files = (list | None),
            source_format = (FileFormat | str | None),
            target_format = (FileFormat | str | None),
            **kwargs):
        """thing that directs files where they need to go
        and deals with certain  kwargs

        Arguments:
            separated_file_list -- a dict of sets of the .docx and .txt
            files separated
        Keyword arguments:
            search_method -- a str (later make this a literal) saying which
            search method to use
            font -- in the case of the font search, which font to search by
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

        keywordprocessors =  collect_keywordprocessors(
            self.source_format,
            self.target_format,
            )

        for i in self.docx_files:
            docx_transliterand = TransliterandFile(
                i,
                self.source_format,
                self.target_format
                )

            transliterated_docx_files.append(
                docworker.transliterate_docx_wordlist(docx_transliterand, keywordprocessors))

        return transliterated_docx_files

    def transliterate_txt(
        self
        ):
        """transliterate a list of txt files

        NOTE: for now I think the only reason why there is a separate function
        is to have accounted for the possibility of the "font" search capability
        which should probably be deprecated
        """
        if self.txt_files is None:
            return []

        transliterated_txt_files = []

        keywordprocessors = collect_keywordprocessors(
            self.source_format,
            self.target_format
            )

        for i in self.txt_files:
            txt_transliterand = TransliterandFile(
                i,
                self.source_format,
                self.target_format
                )
            
            transliterated_txt_files.append(
                txtworker.transliterate_txt_wordlist(
                txt_transliterand,
                keywordprocessors
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

def collect_keywordprocessors(*file_formats):
    
    collected_kps = dict()
    english_keywordprocessor = prepare_engkeywordprocessor()
    collected_kps.update({"english": english_keywordprocessor})
    for i in file_formats:
        hulq_keywordprocessor = prepare_hulqkeywordprocessor(i)
        collected_kps.update({i.to_string(): hulq_keywordprocessor})

    return collected_kps
    


def prepare_engkeywordprocessor():
    eng_wordlist_filepath = wordlist_paths.get("words_alpha_vowels_longer_words")

    eng_keywordprocessor = KeywordProcessor()
    eng_keywordprocessor.add_keyword_from_file(eng_wordlist_filepath)

    return eng_keywordprocessor

def prepare_hulqkeywordprocessor(file_format: FileFormat, **kwargs) -> dict:
    """opens up wordlists for transliteration

    Arguments:
        source_format -- the source format to be transliterated
    Kwargs:
        --update-wordlist: opens the other format wordlists if they are supposed to be
        updated
    """

    def get_non_word_boundary_chars(text_format: FileFormat):
        """gets all of the characters that might not be in [a-zA-Z] or whatever

        Arguments:
            text_format -- a FileFormat of some source
        """
        non_word_boundary_chars = (i for i in GraphemesDict(text_format).source_format_characters)
        return non_word_boundary_chars

    file_format_name = file_format.to_string()
    hulq_wordlist_filename = f'hulq-wordlist-{file_format_name}'
    hulq_wordlist_filepath = wordlist_paths.get(hulq_wordlist_filename)

    hulq_keywordprocessor = KeywordProcessor()
    hulq_keywordprocessor.set_non_word_boundaries(get_non_word_boundary_chars(file_format))
    hulq_keywordprocessor.add_keyword_from_file(hulq_wordlist_filepath)
    return hulq_keywordprocessor


    for i in get_non_word_boundary_chars(file_format):
        hulq_keywordprocessor.add_non_word_boundary(i)
    hulq_keywordprocessor.non_word_boundaries.remove('_')
    hulq_keywordprocessor.add_keyword_from_file(hulq_wordlist_filepath)

    # add wordlists to keywordprocessors
    hulq_keywordprocessor.add_keyword_from_file(hulq_wordlist_filepath)

    return hulq_keywordprocessor

    # if you are going to update the other wordlists
    # def get_wordlists_for_update(source_format: FileFormat):
    # if kwargs.get('update_wordlists'):
    #     wordlists_to_update = get_wordlists_for_update(source_format)
    # all_keyword_processors.update(wordlists_to_update)
    # else:
    #     wordlists_to_update = {}

    # """prepares the wordlists into keyboardprocessors to update

    # Arguments:
    #     source_format -- a FileFormat of the source format

    # Returns:
    #     a dict {'x_keywordprocessor_update' : KeywordProcessor(x), 
    #             {'y_keywordprocessor_update' : KeywordProcessor(y)}
    #         for the two formats, ready to update
    # """

    # # get all the file formats in one set
    # file_format_vals = {i.to_string() for i in FileFormat.file_formats()}

    # # remove the source format (wordlist already opened up)
    # file_format_vals.remove(source_format.to_string())
    # unused_source_formats = {FileFormat.from_string(i) for i in file_format_vals}

    # # collect the keyword processors with the other fileformats
    # update_keywordprocessors = dict()
    # for i in unused_source_formats:
    #     wordlist_update_path = Path(__file__).parent / (
    #                                 'resources/wordlists/hulq-wordlist-' +
    #                                 i.to_string() +
    #                                 '.txt')
        
    #     # make keywordprocessor for each
    #     keywordprocessor_to_update = KeywordProcessor()
    #     for j in get_non_word_boundary_chars(i):
    #         keywordprocessor_to_update.add_non_word_boundary(j)
    #     keywordprocessor_to_update.non_word_boundaries.remove('_')

    #     # add whatever is in their wordlists
    #     keywordprocessor_to_update.add_keyword_from_file(wordlist_update_path)
    #     update_keywordprocessors.update(
    #     {i.to_string() + '_keywordprocessor_to_update' : keywordprocessor_to_update})
    
    # return update_keywordprocessors

    
    

if __name__ == "__main__":
    ...
    