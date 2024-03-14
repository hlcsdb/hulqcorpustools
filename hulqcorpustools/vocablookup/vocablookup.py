
from collections import Counter
import os
from pathlib import Path

from docx import Document as load_docx
from docx.document import Document
import pandas as pd
from dotenv import load_dotenv
from werkzeug.datastructures import FileStorage, ImmutableMultiDict

from hulqcorpustools.resources.wordlists import Wordlist
from hulqcorpustools.resources.constants import TextFormat
from hulqcorpustools.utils.files import FileHandler
from hulqcorpustools.utils.textcounter import TextCounter


class Vocab():
    """Base class for vocab finding functionality. Includes pandas dataframe of
    wordlist
    """
    def __init__(
            self,
            vocab_db=None,
            ):
        
        self.vocab_db = vocab_db
        self.vocab_df = pd.read_csv(
            self.vocab_db,
            index_col='ID',
            keep_default_na=False)


    def defined(self, text_format: TextFormat):
        return set(self.vocab_df[text_format])

    def recognized(self, text_format: TextFormat):
        return {
            self.normalize(word) for word in Wordlist(text_format).words
            }

    def normalize(self, _word: str) -> str:
        """Strip any extraneous characters included on a word.

        Args:
            _word (str): Some word as separated by whitespace.

        Returns:
            str: Word stripped of extraneous characters.
        """
        return _word.strip("— ,.?![]()\"“”.…–1234567890*")


class VocabFinder():

    def __init__(
            self,
            text_format: TextFormat,
            vocab: Vocab):
        """Initialize based on text format.
        Args:
            text_format (FileFormat): the text format to load dictionary
            information for.
        """
        self.text_format = text_format
        self.vocab = vocab
        self.vocab_df = self.vocab.vocab_df
        self.defined = self.vocab.defined(self.text_format)
        self.recognized = self.vocab.recognized(self.text_format)
        self.count_defined = Counter()
        self.count_recognized = Counter()
        self.count_unrecognized = Counter()

    def find_vocab_list(self, text_list: list):

        for text_line in text_list:
            _main_format = kp.determine_text_format(text_line)

            if _main_format == self.text_format:
                for _word in text_line.split():
                    _word = self.vocab.normalize(_word)
                    if _word in self.defined:
                        self.count_defined.update({_word})
                    elif _word in self.recognized:
                        self.count_recognized.update({_word})
                    else:
                        self.count_unrecognized.update({_word})

    def find_vocab(self, _text: str):
        
        # split text into lines and sanitize
        text_list = (
            text_line.strip() for text_line in _text.split('\n')
        )
        self.find_vocab_list(text_list)
    
    def reset_found_words(self):
        self.count_defined = self.count_defined.clear()
        self.count_recognized.clear()
        self.count_unrecognized.clear()

    def update_dataframe_counts(self):
        """
        """
        _counted_defined = self.count_defined.keys()

        # extremely ugly Pandas queries :(

        # make a copy of the vocab df filtering only words that have been found
        self.defined_df = self.vocab_df[self.vocab_df[self.text_format].isin(_counted_defined)].copy()

        self.defined_df['count'] = self.defined_df[self.text_format].map(self.count_defined)
        self.defined_df.sort_values('count', inplace=True, ascending=False)

    @property
    def results(self) -> dict:
        """Return vocab list from df in class as dict.

        Returns:
            dict: _description_
        """
        self.update_dataframe_counts()

        return {
            "defined": self.defined_df.to_dict(orient="index"),
            "recognized": self.count_recognized,
            "unrecognized": self.count_unrecognized
        }

    def update_dataframe_with_line_numbers(self):
        """TODO: give first line number as well as all other line numbers
        where word appears

        Returns:
            _type_: _description_
        """
        ...


class VocabFinderFile(VocabFinder):
    """VocabFinder specifically for searching files for vocab words.
    """
    def __init__(
            self,
            text_format: TextFormat,
            vocab: Vocab,
            file_list: list[FileStorage],
            ):
        """Instantiate a VocabFinder based on a FileFormat and prepare to read
        from a file list.

        Args:
            text_format (FileFormat | str): _description_
            files_list (list[Path]): _description_
        """
        self.file_list = file_list
        self.text_format = text_format
        self.vocab = vocab
        super().__init__(self.text_format, self.vocab)
        self._find_vocab = self.find_vocab
        self.file_handler = FileHandler(self.file_list)

    def find_vocab(
            self,
            ) -> dict:

        text_list = []
        for _file in self.file_handler.docx_files:
            file_docx = load_docx(_file) # type: Document
            text_list.extend([
                par.text for par in file_docx.paragraphs])

            for table in file_docx.tables:
                for row in table.rows:
                    for cell in row.cells:
                        text_list.extend([cell.text])

        for _file in self.file_handler.txt_files:
            with open(_file) as _open_file:
                text_list = [_line for _line in _open_file]

        self.find_vocab_list(text_list)