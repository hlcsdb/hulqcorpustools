
from pathlib import Path
from importlib.resources import files
from hulqcorpustools.resources.constants import TextFormat

wordlist_package = files(__package__) / 'wordlistsdata'
wordlist_paths = {Path(wordlist_path).stem : wordlist_path for wordlist_path in wordlist_package.iterdir()}

class Wordlist():

    # ENGLISH_WORDLIST_TEXT = imp_resources.read_text(wordlistsdata, "english-wordlist.txt")

    @staticmethod
    def load_wordlist_text(
        wordlist_format: str|TextFormat) -> str:
        """_summary_

        ***REMOVED***rguments:
            wordlist_format -- _description_
        """
        
        if type(wordlist_format) == TextFormat:
            wordlist_format = wordlist_format.to_string()

        if wordlist_format == 'english':
            _filename = 'english-wordlist.txt'

        else:
            _filename = f"hulq-wordlist-{wordlist_format}.txt".casefold()

        return open(wordlist_package.joinpath(_filename))

    ENGLISH_WORDLIST_TEXT = load_wordlist_text("english")
    ORTHOGRAPHY_WORDLIST_TEXT = load_wordlist_text("orthography")
    APA_UNICODE_WORDLIST_TEXT = load_wordlist_text("apaunicode")
    STRAIGHT_WORDLIST_TEXT = load_wordlist_text("straight")

if __name__ == "__main__":
    for i in Wordlist.APA_UNICODE_WORDLIST_TEXT:
        print(i)