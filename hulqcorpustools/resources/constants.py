from enum import Enum, StrEnum, auto
import json
from pathlib import Path
from importlib.resources import files

__package__ = "hulqcorpustools.resources"


class TextFormat(StrEnum):
    """The possible text formats that some doc can be in.

        'Straight': Only for use as a source file. An old interim solution
        for rendering APA characters correctly using a specific font called
        Straight when there was no Unicode support.
        'orthography': Practical orthography written with conventional
        keyboard characters.
        'APAUnicode': APA (Americanist Phonetic Alphabet) written with Unicode
        characters.
    """

    STRAIGHT = auto()
    APAUNICODE = auto()
    ORTHOGRAPHY = auto()
    ENGLISH = auto()

    @property
    def is_lang_format(self):
        """Returns whether or not the Text Format is in a language other than English.
        """
        return self in {self.STRAIGHT, self.APAUNICODE, self.ORTHOGRAPHY}

    def to_string(self):
        if self == self.APAUNICODE:
            file_format_str = 'APAUnicode'
        else:
            file_format_str = self.name.lower()

        return file_format_str

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
        return self.value


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
    """Correspondence of graphemes for Hul’q’umi’num’.
    """
    grapheme_file = files(__package__) / "graphemes.json"

    def text_format_graphemes(
            self,
            text_format: TextFormat,
            grapheme_kind: Grapheme
            ) -> set:
        """Get the characters for a given TextFormat (i.e. all possible
        renderings) of that grapheme.

        Args:
            text_format (TextFormat): _description_
        """
        return list({
            grapheme.get(text_format).get(grapheme_kind): None
            for grapheme in self.graphemes
            })

    def correspondence_dict(
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
            for grapheme in self.graphemes
        }

    @property
    def graphemes(self):
        return json.load(open(self.grapheme_file))

    # def __repr__(self):
    #     return str(self.graphemes)
