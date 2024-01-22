""" a spellchecker for hul’q’umi’num’ language

# WHAT WAAS THE PROCEDURE FOR PUTTING TOGETHER THIS SPELLCHECKER?

1. take a wordlist of some form, in this case, parsed from the Hukari & Peter
excel dictionary as it is apparently the most up-to-date one
2. parse the wordlist for just each individual entry to get a file with just
each word on each line
3. make a KeywordProcessor of the wordlist to use the flashtext algorithm
for quick membership checking (this is done in the *hwordlists* package)
4. extract tokens from the corpus: only look at lines that start with LH; then,
for each word in the line, if that word is in the wordlist, count it; if not, ignore
(This is because words not in the wordlist have not been checked for spelling. These
words will be interesting for further study or for future spellchecking, but they have
not yet been vetted)
5. Write the frequency of these words. For the remainder of the words found in the
wordlist but not in the corpus, add these to the overall frequency count
6. next is to give this to the spellchecker...
"""

import json
from pathlib import Path
from spellchecker import SpellChecker

hulq_spellchecker = SpellChecker(language=None)

data_path = Path(__file__).resolve().parent.parent / 'hulqwordfrequency' / 'output'
word_frequency_json_path = data_path.joinpath('word_frequency_wordlist_incl.json')
hulq_spellchecker_gz_path = data_path.joinpath('hulq_spellchecker.gz')
    
def build_hulq_spellchecker():
    """builds spellchecker to usual specs
    """
    with open(word_frequency_json_path, 'r') as word_frequency_json_file:
        frequency_json = json.load(word_frequency_json_file)
        hulq_spellchecker.word_frequency.load_json(frequency_json)

    hulq_spellchecker.export(str(Path(word_frequency_json_path.joinpath('hulq_spellchecker.gz'))), gzipped=True)

def load_hulq_spellchecker(spellchecker):
    """loads the spellchecker saved as gz
    """
    spellchecker.word_frequency.load_dictionary(str(hulq_spellchecker_gz_path), encoding='utf-8')


if __name__ == '__main__':
    load_hulq_spellchecker(hulq_spellchecker)

    