
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path
from importlib.resources import files
from hulqcorpustools.resources.constants import TextFormat
from hulqcorpustools.resources import data

class Wordlists():
        
    def __init__(self, text_formats: Iterable[TextFormat]):
        self.wordlists = {
            text_format: Wordlist(text_format)
            for text_format in text_formats
        }

    def __repr__(self):
        return self.wordlists

class Wordlist():
    
    data = data
    paths = files(data)

    def __init__(self, text_format: TextFormat):
        self.filename = f"{text_format}-wordlist.txt"
        self.path = self.paths.joinpath(self.filename) # type: Path
        with open(self.path, "r") as f:
            self.words = {word.strip() for word in f}
        self.text_format = text_format
