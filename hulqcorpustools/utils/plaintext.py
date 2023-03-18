
from pathlib import Path
from typing import Optional
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