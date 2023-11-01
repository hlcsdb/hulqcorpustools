import pandas as pd

from hulqcorpustools.resources import wordlists
from hulqcorpustools.utils.keywordprocessors import HulqKeywordProcessors

_hulq_kp = HulqKeywordProcessors(eng=True)

class VocabLookup():

    def __init__(self):
        self.hukari_peter_parses_df = pd.read_csv(wordlists.wordlist_package / 'hukari-peter-parses.csv', index_col='LEXEME - curly ’unuhw')

    def get_hulq_words(self, textline: str):
        _hulq_kp.determine_language_from_text(textline)