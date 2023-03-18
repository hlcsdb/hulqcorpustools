
from importlib import resources as imp_resources

from . import wordlistsdata
from .constants import FileFormat

class Wordlist():

    # ENGLISH_WORDLIST_TEXT = imp_resources.read_text(wordlistsdata, "english-wordlist.txt")

    def load_wordlist_text(
        wordlist_format: str|FileFormat) -> str:
        """_summary_

        ***REMOVED***rguments:
            wordlist_format -- _description_
        """

        if type(wordlist_format) == FileFormat:
            wordlist_format = wordlist_format.to_string()

        if wordlist_format == 'english':
            return imp_resources.read_text(wordlistsdata, "english-wordlist.txt")

        else:
            _filename = f"hulq-wordlist-{wordlist_format}.txt"
            return imp_resources.read_text(wordlistsdata, _filename)

    ENGLISH_WORDLIST_TEXT = load_wordlist_text("english")
    ORTHOGRAPHY_WORDLIST_TEXT = load_wordlist_text("orthography")
    APA_UNICODE_WORDLIST_TEXT = load_wordlist_text("APA-unicode")
    STRAIGHT_WORDLIST_TEXT = load_wordlist_text("straight")
    
    # HULQ_WORDLISTS = (load_wordlist_text(_file_format) for _file_format in FileFormat.HULQ_FORMATS)


if __name__ == "__main__":
    ...