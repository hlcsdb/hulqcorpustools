
from pathlib import Path
from typing import Optional

from flashtext import KeywordProcessor as kp

from hulqcorpusresources.constants import FileFormat
from hulqcorpusresources.wordlists import Wordlist

import re

hulqletters = re.compile(r'a-zA-Z’')
rl = re.compile('([aeiou][\.|\-]){2,}')
strip_punctuation = re.compile('[\.|,|?|“|"|”|\[|\]|1|2|3|4|5|6|7|8|9|0|\(|\)]')
is_number = re.compile('[0-9]+')

def strip_rl_and_punc(word: str) -> str:
    '''strips off rhetorical lengthening (if any) and extraneous punctuation'''

    word_sub = lambda x: strip_punctuation.sub('', rl.sub(r'\1', x))
    
    if len(word_sub(word)) == 0:
        return(word)

    return(word_sub(word))

def _load_flashtext(
    _wordlist_format: str | None
    ):

    
    if _wordlist_format is None:
        _wordlist = Wordlist.ORTHOGRAPHY_WORDLIST_TEXT

    else:
        _wordlist = Wordlist.load_wordlist_text(_wordlist_format)

    _wordlist = _wordlist.split()

    _hulq_kp = kp()
    _hulq_kp.add_non_word_boundary('’')
    _hulq_kp.add_keywords_from_list(
        _wordlist
            )

    return _hulq_kp


def _determine_language_for_line(
    linetext: str,
    hulq_kp: kp,
    english_kp: kp) -> FileFormat:
    """determines which language the line is in

    Arguments:
        linetext -- _description_
        hulq_kp -- _description_
        english_kp -- _description_

    Returns:
        _description_
    """


    hulq_count = 0
    english_count = 0
    found_hulq_words = hulq_kp.extract_keywords(linetext)
    found_english_words = english_kp.extract_keywords(linetext)

    print(found_hulq_words, found_english_words)
    ...