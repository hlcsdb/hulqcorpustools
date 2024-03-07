
from pathlib import Path
from importlib.resources import files
from hulqcorpustools.resources.constants import TextFormat
from hulqcorpustools.resources import data




class Wordlist():

    data = data
    paths = files(data)

    def __init__(self, text_format: TextFormat):
        self.filename = f"{text_format}-wordlist.txt"
        self.path = self.paths.joinpath(self.filename) # type: Path
        self.file = open(self.paths.joinpath(self.filename))
        self.words = {word.strip() for word in self.file}

if __name__ == "__main__":
    print(Wordlist(TextFormat.ORTHOGRAPHY).path)
