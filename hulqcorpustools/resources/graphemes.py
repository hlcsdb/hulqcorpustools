
from enum import Enum, auto
from importlib.resources import files
import json

from hulqcorpustools.resources.constants import TextFormat

grapheme_file = files(__package__) / "graphemes.json"
graphemes = json.load(open(grapheme_file))


class Grapheme(Enum):
    CHARACTERS = auto()
    LEMMA = auto()

    def __str__(self):
        return self.casefold()


def text_format_chars(
        text_format: TextFormat,
        grapheme_kind: Grapheme
        ) -> set:
    """Get the characters for a given TextFormat (i.e. all possible renderings)
    of that grapheme.

    Args:
        text_format (TextFormat): _description_
    """
    return {
        grapheme.get(text_format).get(grapheme_kind) for grapheme in graphemes
        }

if __name__ == "__main__":
    ...