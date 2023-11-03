
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

        self.parses_df = pd.read_csv(wordlists.wordlist_package / 'hukari-peter-parses.csv', index_col=self.text_format_str, keep_default_na=False)
        self.defined_words = set(self.parses_df.index.values)

        self.count_defined_words = Counter()
        # self.found_defined_words = set()
        self.found_known_words = set()
        self.found_unknown_words = set()


    def reg_word(self, _word: str) -> str:
        return _word.strip(" ,.?![]()\"“”.…")

    def get_all_hulq_words_in_line(self, _textline: str):
        """get all hulq words from any line of text
        """
        _main_language = _hulq_kp.determine_language_from_text(_textline)
        if _main_language == self.text_format:
            for _word in _textline.split():
                _word = self.reg_word(_word)
                if _word in self.defined_words:
                    self.count_defined_words.update({_word})
                    # self.found_defined_words.add(_word)
                elif _word in self.text_format_wordlist:
                    self.found_known_words.add(_word)
                else:
                    self.found_unknown_words.add(_word)

    @property
    def vocab(self) -> pd.DataFrame:
        _found_words = self.count_defined_words
        self.defined_words_df = self.parses_df.query('index in @_found_words').copy()
        self.defined_words_df['counts'] = self.defined_words_df.index.map(self.count_defined_words)


        return self.defined_words_df