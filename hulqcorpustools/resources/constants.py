from enum import StrEnum, auto
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

    @classmethod
    def lang_format(cls):
        return {cls.STRAIGHT, cls.APAUNICODE, cls.ORTHOGRAPHY}

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

