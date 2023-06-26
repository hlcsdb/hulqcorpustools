
from pathlib import Path
from importlib.resources import files
from hulqcorpustools.resources.constants import FileFormat

wordlist_package = files(__package__) / 'wordlistsdata'
wordlist_paths = {Path(wordlist_path).stem : wordlist_path for wordlist_path in wordlist_package.iterdir()}

class Wordlist():

    # ENGLISH_WORDLIST_TEXT = imp_resources.read_text(wordlistsdata, "english-wordlist.txt")

    @staticmethod
    def load_wordlist_text(
        wordlist_format: str|FileFormat) -> str:
        """_summary_

        ***REMOVED***rguments:
            wordlist_format -- _description_
        """
        
        if type(wordlist_format) == FileFormat:
            wordlist_format = wordlist_format.to_string()

        if wordlist_format == 'english':
            return open(wordlist_package.joinpath('english-wordlist.txt'))

        else:
            _filename = f"hulq-wordlist-{wordlist_format}.txt"
            return open(wordlist_package.joinpath(_filename))

    

    ENGLISH_WORDLIST_TEXT = load_wordlist_text("english")
    ORTHOGRAPHY_WORDLIST_TEXT = load_wordlist_text("orthography")
    APA_UNICODE_WORDLIST_TEXT = load_wordlist_text("APAunicode")
    STRAIGHT_WORDLIST_TEXT = load_wordlist_text("straight")
    
    # HULQ_WORDLISTS = (load_wordlist_text(_file_format) for _file_format in FileFormat.HULQ_FORMATS)


if __name__ == "__main__":
    for i in Wordlist.APA_UNICODE_WORDLIST_TEXT:
        print(i)