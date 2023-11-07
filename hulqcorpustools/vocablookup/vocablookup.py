
from collections import Counter

import pandas as pd

from hulqcorpustools.resources import wordlists
from hulqcorpustools.resources.constants import FileFormat
from hulqcorpustools.utils.keywordprocessors import HulqKeywordProcessors

_hulq_kp = HulqKeywordProcessors(eng=True)

class VocabLookup():
    def __init__(self, text_format: FileFormat):
        self.text_format = text_format
        self.text_format_str = text_format.to_string().upper()
        self.text_format_wordlist = {i.strip() for i in wordlists.Wordlist.load_wordlist_text(self.text_format)}

        self.parses_df = pd.read_csv(wordlists.wordlist_package / 'hukari-peter-parses.csv', index_col='ID', keep_default_na=False)
        self.defined_words = set(self.parses_df[self.text_format_str].values)

        self.count_defined_words = Counter()
        # self.found_defined_words = set()
        self.found_known_words = set()
        self.found_unknown_words = set()


    def reg_word(self, _word: str) -> str:
        return _word.strip(" ,.?![]()\"“”.…")

    def collect_hulq_words_in_textline(self, _textline: str):
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

    def collect_hulq_words_in_text(self, _text: str):
        for _textline in _text.split('\n'):
            self.collect_hulq_words_in_textline(_textline)

    def reset_found_words(self):
        self.count_defined_words = Counter()
        self.found_known_words = set()
        self.found_unknown_words = set()

    @property
    def vocab(self) -> pd.DataFrame:
        _found_words = self.count_defined_words
        _text_format = self.text_format_str
        self.defined_words_df = self.parses_df[self.parses_df[_text_format].isin(_found_words)].copy()

        self.defined_words_df['COUNT'] = self.defined_words_df[_text_format].map(self.count_defined_words)


        return self.defined_words_df