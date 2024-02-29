
from collections import Counter
from pathlib import Path

import pandas as pd
from docx import Document as init_doc
from docx.document import Document

from hulqcorpustools.resources import wordlists
from hulqcorpustools.resources.constants import TextFormat
from hulqcorpustools.utils.files import FileHandler
from hulqcorpustools.utils.keywordprocessors import HulqKeywordProcessors as kp


class _BaseVocabFinder():
    """Base class for vocab finding functionality. Includes pandas dataframe of
    wordlist (TODO: perhaps should be separated out later.)
    """
    def __init__(self, text_format: TextFormat | str):
        if isinstance(text_format, str):
            text_format = TextFormat.from_string(text_format)
        self.text_format = text_format
        self.text_format_str = text_format.to_string().upper()
        self.text_format_wordlist = {i.strip() for i in wordlists.Wordlist.load_wordlist_text(self.text_format)}

        # Initiate Pandas dataframe of wordlist
        self.parses_df = pd.read_csv(
            wordlists.wordlist_package / 'hukari-peter-parses.csv',
            index_col='ID',
            keep_default_na=False)

        # The words from the Pandas dataframe i.e. those that are defined.
        # Checking membership in set should be much faster than looking in df.
        self.defined_words = set(self.parses_df[self.text_format_str].values)

        self.count_defined_words = Counter()
        self.count_known_words = Counter()
        self.found_unknown_words = set()

    def normalize_word(self, _word: str) -> str:
        """Strip any extraneous characters included on a word.

        Args:
            _word (str): Some word as separated by whitespace.

        Returns:
            str: Word stripped of extraneous characters.
        """
        return _word.strip("— ,.?![]()\"“”.…–1234567890")

    def update_dataframe_with_counts(self):
        """Update the dataframe to include the figures from counting instances of
        known and recognized words and sort by count.

        This is put in its own function as making and/or updating a new DF is
        fairly expensive, whereas updating a counter is not.

        Returns:
            _type_: _description_
        """
        _found_words = self.count_defined_words.keys()

        # extremely ugly Pandas queries :(

        self.defined_words_df = self.parses_df[self.parses_df[self.text_format_str].isin(_found_words)].copy()

        self.defined_words_df['COUNT'] = self.defined_words_df[self.text_format_str].map(self.count_defined_words)
        self.defined_words_df.sort_values('COUNT', inplace=True, ascending=False)

    def update_dataframe_with_line_numbers(self):
        """TODO: give first line number as well as all other line numbers
        where word appears

        Returns:
            _type_: _description_
        """
        ...

    def find_hulq_words_in_text(self, _textline: str):
        """Get all words in a line of text and update counters.
         
        The counters are of words that have definitions,
        words that are recognized but not defined, and
        words that are unrecognized (so are present in a line where it is 
        determined to be in Hul’q’umi’num’, but aren't on any wordlist.

        Args:
            _textline (str): Any line of text. In this function it is determined
              to be in Hul’q’umi’num’ or English.
        """
        # first: see if line of text is largely in hulq at all
        _textline = _textline.strip()
        _main_textline_language = _hulq_kp.determine_language_from_text(_textline)

        if _main_textline_language == self.text_format:
            for _word in _textline.split():
                _word = self.normalize_word(_word)

                if _word in self.defined_words:
                    self.count_defined_words.update({_word})
                elif _word in self.text_format_wordlist:
                    self.count_known_words.update({_word})
                else:
                    self.found_unknown_words.add(_word)


    def find_hulq_words_in_text_list(self, _textlist: list[str]):
        """Get Hul’q’umi’num’ words from an already-separated list of words.

        Args:
            _textlist (list[str]): A list of words.
        """
        for _textline in _textlist:
            self.find_hulq_words_in_text(_textline)

    def find_hulq_words_in_multiline_string(self, _text: str):
        _textlines = _text.split('\n')
        self.find_hulq_words_in_text_list(_textlines)

    def reset_found_words(self):
        self.count_defined_words = Counter()
        self.found_known_words = set()
        self.found_unknown_words = set()

    @property
    def vocab_df(self) -> pd.DataFrame:
        """Sort/prepare dataframe to be turned into data elsewhere.
        """
        self.update_dataframe_with_counts()
        return self.defined_words_df

    @property
    def vocab(self) -> dict:
        """Return vocab list from df in class as dict.

        Returns:
            dict: _description_
        """
        _vocab = {
            'defined_words': self.vocab_df.to_dict(orient='index'),
            'known_words': self.count_known_words,
            'unknown_words': self.found_unknown_words
        }

        return _vocab

class VocabFinder(_BaseVocabFinder):
    """Class for initializing and delegating to VocabFinders based on text format.

    This mostly provides a simpler interface to vocab finding functions and to
    instantiate a single _BaseVocabFinder for looking up in multiple files.

    The intended usage is to initialize a VocabFinder with a FileFormat and to
    pass it some text or a file with the find_vocab... methods. It finds and
    counts all of the vocab in all given files and changes them as attributes.

    When ready, the data is requested with the .vocab property, at which point
    it is compiled and converted to a dict.
    """

    def __init__(
            self,
            text_format: TextFormat | str):
        """Initialize based on text format.
        Args:
            text_format (FileFormat | str): the text format to load dictionary
            information for. Receives FileFormat or string to deal with getting
            a string from html request.
        """
        self.text_format = text_format
        super().__init__(self.text_format)

    def find_vocab_in_text(
            self,
            _text: str,
            ) -> dict:
        """Look up all of the hulq words in a single text string.
          This string could be very long, e.g., if the user copies and pastes
           a whole document into a text box form.
        Args:
            _text (str): the text to find the vocab in
        Returns:
            dict: a dict containing the words and their dictionary data
        """

        self.find_hulq_words_in_multiline_string(_text)

class VocabFinderFile(_BaseVocabFinder):
    """VocabFinder specifically for searching files for vocab words.
    """
    def __init__(
            self,
            text_format: TextFormat | str,
            file_list: list[Path]
            ):
        """Instantiate a VocabFinder based on a FileFormat and prepare to read
        from a file list.

        Args:
            text_format (FileFormat | str): _description_
            files_list (list[Path]): _description_
        """
        self.file_list = file_list
        super().__init__(text_format)

    def find_vocab_in_file(
            self,
        _file: Path,
            ) -> dict:
        """Look up all of the Hul’q’umi’num’ words in one file.

        Every time this function is called, the class attributes are updated.

        Args:
            _file (Path): a .txt or .docx file (.doc files are converted
            by FileHandler provided already)

        Returns:
            dict: a dict containing the words and their dictionary data
        """
        textline_list = []
        if _file.suffix == '.docx':
            file_docx = init_doc(_file) # type: Document
            textline_list.extend([par.text for par in file_docx.paragraphs])

            for table in file_docx.tables:
                for row in table.rows:
                    for cell in row.cells:
                        textline_list.extend([cell.text])
        
        elif _file.suffix == '.txt':
            with open(_file) as _open_file:
                textline_list = [_line for _line in _open_file]

        self.find_hulq_words_in_text_list(textline_list)

    def find_vocab_in_files(self):
        for _file in self.file_list:
            self.find_vocab_in_file(_file)

