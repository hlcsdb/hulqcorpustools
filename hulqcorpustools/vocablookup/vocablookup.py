
from collections import Counter
from pathlib import Path

import pandas as pd
from docx import Document as init_doc
from docx.document import Document

from hulqcorpustools.resources import wordlists
from hulqcorpustools.resources.constants import FileFormat
from hulqcorpustools.utils.files import FileHandler
from hulqcorpustools.utils.keywordprocessors import HulqKeywordProcessors

_hulq_kp = HulqKeywordProcessors(eng=True)

class _BaseVocabFinder():
    """base class for vocab finding functionality
    """
    def __init__(self, text_format: FileFormat):
        self.text_format = text_format
        self.text_format_str = text_format.to_string().upper()
        self.text_format_wordlist = {i.strip() for i in wordlists.Wordlist.load_wordlist_text(self.text_format)}

        self.parses_df = pd.read_csv(wordlists.wordlist_package / 'hukari-peter-parses.csv', index_col='ID', keep_default_na=False)
        self.defined_words = set(self.parses_df[self.text_format_str].values)

        self.count_defined_words = Counter()
        self.found_known_words = set()
        self.found_unknown_words = set()

    def reg_word(self, _word: str) -> str:
        return _word.strip("— ,.?![]()\"“”.…–1234567890")

    def find_hulq_words_in_textline(self, _textline: str):
        """get all hulq words from any line of text
        """
        # first: see if line of text is largely in hulq at all
        _main_textline_language = _hulq_kp.determine_language_from_text(_textline)
        if _main_textline_language == self.text_format:
            for _word in _textline.split():
                _word = self.reg_word(_word)
                if _word in self.defined_words:
                    self.count_defined_words.update({_word})
                elif _word in self.text_format_wordlist:
                    self.found_known_words.add(_word)
                else:
                    self.found_unknown_words.add(_word)

    def find_hulq_words_in_text_list(self, _textlist: list[str]):
        for _textline in _textlist:
            self.find_hulq_words_in_textline(_textline)

    def find_hulq_words_in_string(self, _text: str):
        _textlines = _text.split('\n')
        self.find_hulq_words_in_text_list(_textlines)

    def reset_found_words(self):
        self.count_defined_words = Counter()
        self.found_known_words = set()
        self.found_unknown_words = set()



    @property
    def vocab(self) -> pd.DataFrame:
        """sort/prepare df to be turned into data elsewhere
        """
        _found_words = self.count_defined_words
        _text_format = self.text_format_str
        self.defined_words_df = self.parses_df[self.parses_df[_text_format].isin(_found_words)].copy()
        self.defined_words_df['COUNT'] = self.defined_words_df[_text_format].map(self.count_defined_words)
        self.defined_words_df.sort_values('COUNT', inplace=True, ascending=False)
        return self.defined_words_df

class VocabFinder(_BaseVocabFinder):
    """class for initializing and delegating to VocabFinders based on text format
    """

    def __init__(
            self,
            text_format: FileFormat | str):
        
        if isinstance(text_format, str):
            text_format = FileFormat.from_string(text_format)

        self.text_format = text_format
        super().__init__(self.text_format)

    def lookup_string(
            self,
            _text: str,
            ) -> dict:
        """look up all of the hulq words in a single text string (which could be very long, e.g. copying and pasting a whole document)

        Arguments:
            _text -- the text to find the vocab in

        Returns:
            dict of the results
        """

        self.find_hulq_words_in_string(_text)
        return self.all_results


    def lookup_file(
            self,
            _file: Path,
             ) -> dict:
        """look up all of the hulq words in one file

        Arguments:
            _file -- a .txt or .docx file (.doc files are converted by FileHandler provided already)

        Returns:
            dict of the results
        """
        file_docx = init_doc(_file) # type: Document
        textline_list = []
        textline_list.extend([par.text for par in file_docx.paragraphs])

        for table in file_docx.tables:
            for row in table.rows:
                for cell in row.cells:
                    textline_list.extend([cell.text])

        self.find_hulq_words_in_text_list(textline_list)

        return self.all_results

    @property
    def all_results(self):
        results = {
            'vocab_found': self.vocab.to_dict(orient='index'),
            'known_words': list(self.found_known_words),
            'unknown_words': list(self.found_unknown_words)
        }

        return results

class VocabFinderFilehandler(FileHandler):

    def __init__(
            self,
            files_list = list[Path],
            text_format = FileFormat | str
            ):
        super().__init__(files_list)

        self.vf = VocabFinder(text_format)
        self.find_vocab_in_files()
        self.all_results = self.vf.all_results

    def find_vocab_in_files(self):
        for _file in self.docx_files:
            self.vf.lookup_file(_file)
            return self.vf.all_results