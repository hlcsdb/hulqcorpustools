"""control room for the transliterator

from here, open files, get line, feed transliterator each line
 can deal with text files here for now, but docworker
will be the place to pull out lines from .docx

"""

from flashtext import KeywordProcessor
from pathlib import Path
import os

import importlib.resources

from ..resources import wordlists as wl
from ..resources.constants import FileFormat, TransliterandFile, GraphemesDict
from ..filehandlers import docworker, txtworker
from . import replaceengine as repl

# TODO: add feature to transliterate *only* hulq words
# may take a much more substantial wordlist

class FileController():
    
    def __init__(self, separated_file_list: dict, **kwargs):
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
        self.docx_files = separated_file_list.get('docx') # Type: set(TransliterandFile)
        self.txt_files = separated_file_list.get('txt') # Type: set(TransliterandFile)
        
        self.search_method = kwargs.get('search_method')
        self.font_search = kwargs.get('font')

        if self.docx_files:
            self.docx_list_controller(self.docx_files)    

        if self.txt_files:
            self.txt_list_controller(self.txt_files)

    @classmethod
    def file_processor(
        cls,
        separated_file_list: dict,
        **kwargs):
        """give this sucker a list of txt files and a list of .docx files
        and it sends it to where it needs to go
        
        Arguments:
            separated_file_list: a dict with a list each of docx and txt
            e.g. {'docx':[file1, file2, ...]}

        kwargs:
            target_destination: where the file is supposed to go; defaults to same
            folder as source file if empty
            font: a target font when processing .docx files
        """

        # what happened to the file to put in filename: straight to APA, etc.

        print(separated_file_list)
        search_type = kwargs.get('search_type')

        if search_type == 'Font':
            _font = kwargs.get('font')
            cls.docx_list_controller(separated_file_list['docx'], font=_font)

        elif search_type == 'Wordlist':
            cls.docx_list_controller(separated_file_list['docx'])


        # if separated_file_list.get('docx'):
        #     docx_list_controller(list(separated_file_list.get('docx')))
        # if separated_file_list.get('txt'):
        #     txt_list_controller(list(separated_file_list.get('txt')))

    @classmethod
    def docx_list_controller(
        cls,
        docx_list: set(),
        **kwargs
        ):
        """manages the list of docx files

        Arguments:
            doc_list -- a set of TransliterandFiles referring to .docx
            source_format -- a FileFormat giving format of the source ifle
            target_format -- a FileFormat giving format of the target file
        Kwargs:
            update-wordlist: updates the Hul’q’umi’num’ wordlists with what gets found
        """ 

        # source_formats = (i.source_format for i in docx_list)
        # print(source_formats)
        # update_wordlists = kwargs.get('update_wordlists')
        # keywordprocessors = {prepare_keywordprocessor(i) for i in source_formats}
        # keywordprocessors = prepare_keywordprocessor(source_format,
                                # update_wordlists=update_wordlists)

        keywordprocessors =  collect_keywordprocessors([FileFormat.STRAIGHT, FileFormat.ORTHOGRAPHY])

        source_format = kwargs.get('sourceformat')
        target_format = kwargs.get('targetformat')

        if kwargs.get('sourceformat') is None:
            source_format = FileFormat.ORTHOGRAPHY
        
        if kwargs.get('targetformat') is None:
            target_format = FileFormat.APAUNICODE

        

        for i in docx_list:
            doc_transliterand = TransliterandFile(i, source_format, target_format)

            docworker.transliterate_docx_wordlist(doc_transliterand, keywordprocessors)

        # for i in docx_list:
        #     docworker.transliterate_docx_font(i, font=kwargs.get('font', None))

    @classmethod
    def txt_list_controller(
        txt_list: set,
        **kwargs
        ):

        update_wordlists = kwargs.get('update')
        source_format = txt_list[0].source_format
        keywordprocessors = collect_keywordprocessors(source_format)

        for i in txt_list:
            txtworker.transliterate_txt_wordlist(i, keywordprocessors, update_wordlists=update_wordlists)

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

def collect_keywordprocessors(file_formats: list[FileFormat]):
    
    _collected = dict()
    english_keywordprocessor = prepare_engkeywordprocessor()
    hulq_keywordprocessors = {file_format.to_string() : prepare_hulqkeywordprocessor(file_format) for file_format in file_formats}

    # print(hulq_keywordprocessors)
    _collected.update({"english": english_keywordprocessor})
    _collected.update(hulq_keywordprocessors)

    return _collected
    



def prepare_engkeywordprocessor():

    wordlist_paths = importlib.resources.files(wl)
    eng_wordlist_filepath = Path(wordlist_paths / "words_alpha_vowels_longer_words.txt")

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

    file_format_name = file_format.to_string()
    wordlist_paths = importlib.resources.files(wl)

    hulq_wordlist_filename = f'hulq-wordlist-{file_format_name}.txt'
    hulq_wordlist_filepath = Path(wordlist_paths / hulq_wordlist_filename)

    # initialize keywordprocessor    
    hulq_keywordprocessor = KeywordProcessor()

    def get_non_word_boundary_chars(text_format: FileFormat):
        """gets all of the characters that might not be in [a-zA-Z] or whatever

        Arguments:
            text_format -- a FileFormat of some source
        """
        non_word_boundary_chars = (i for i in GraphemesDict(text_format).source_format_characters)
        return non_word_boundary_chars

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
    