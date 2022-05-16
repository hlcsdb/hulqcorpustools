import os
from pathlib import Path

def get_wordlist_paths() -> dict:
    """returns a dict of the paths of wordlists relative to everything
    I suppose
    """
    wordlists = {
        i.name : i for i in Path(__file__).parent.glob('*.txt')
    }

    return wordlists

wordlist_paths = get_wordlist_paths()