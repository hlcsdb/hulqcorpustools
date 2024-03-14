
from enum import StrEnum, auto
from itertools import chain
from importlib.resources import files
import json
import string
import re

from hulqcorpustools.resources.constants import TextFormat

__package__ = "hulqcorpustools.resources"


class Grapheme(StrEnum):
    CHARACTERS = auto()
    LEMMA = auto()

    @classmethod
    def _missing_(cls, value):
        """Case-insensitively cast strings of a TextFormat (e.g. "apaunicode")
          to Enum
        """
        value = value.casefold()
        for member in cls:
            if member.value == value:
                return member
            return None
        
    def __str__(self):
        return self.casefold()


class Graphemes():

    @classmethod
    def graphemes(
            cls,
            text_format: TextFormat,
            grapheme_kind: Grapheme,
            grapheme_data: dict
            ) -> set:
        """Get the characters for a given TextFormat (i.e. all possible
        renderings) of that grapheme.

        Args:
            text_format (TextFormat): _description_
        """
        if text_format == TextFormat.ENGLISH:
            return {char for char in string.ascii_lowercase}
        return {
            grapheme.get(text_format).get(grapheme_kind)
            for grapheme in grapheme_data

            }

    def correspondence(
            self,
            source_format: TextFormat,
            target_format: TextFormat
            ):
        """Give the correspondence of certain characters in the source format
        to the lemma in the target. For example, if there are two ways of
        rendering a character for whatever reason in one format, give the best
        rendering (i.e. the lemma) of that character in the target format.

        Args:
            source_format (TextFormat): _description_
            target_format (TextFormat): _description_

        Returns:
            _type_: _description_
        """
        
        return {
            grapheme.get(source_format).get(Grapheme("characters")):
            grapheme.get(target_format).get("lemma")
            for grapheme in self.data
        }

    @classmethod
    def _re_compile(
            cls,
            text_format: TextFormat,
            grapheme_data: dict
        ):
        # print(cls.graphemes(text_format, Grapheme.CHARACTERS, grapheme_data))
        unique_chars = set(chain.from_iterable(cls.graphemes(
            text_format, Grapheme.CHARACTERS, grapheme_data)))
        re_string = re.escape("".join(unique_chars))
        return re.compile(f"[^{re_string}]")

    def __init__(self, text_formats: set[TextFormat]):
        grapheme_file = files(__package__) / "graphemes.json"

        with open(grapheme_file) as _open_file:
            self.data = json.load(_open_file)

        self.re_compiled = {
            _text_format: self._re_compile(_text_format, self.data)
            for _text_format in text_formats
        }

    def sanitize(
        self,
        _text: str,
        _text_format: TextFormat
    ):
        return self.re_compiled.get(_text_format).sub("", _text.casefold())


if __name__ == "__main__":
    ...