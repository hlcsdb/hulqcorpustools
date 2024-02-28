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
    def is_hulq_format(self):
        """Returns whether or not the Text Format is in Hul’q’umi’num’.

        Returns:
            bool: True or False given whether or not the text format is a way of
            rendering Hul’q’umi’num’.
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

class TransliterandFile():
    '''a class that collects a file and its parameters for transliteration

    Arguments:
        source_path: a Path to the source file to be transliterated
        source_format: the FileFormat of the source file
        target_format: the FileFormat that the source file should be
        transliterated into

    Attributes:
        source_path: a Path to the source file to be transliterated
        source_filename: string with just the name of the source file
        (e.g. 'file.docx')
        source_folder: a Path to the folder the source file is in
        (e.g. 'home/folder_with_files/file.docx' -> 'home/folder_with_files)
        suffix: the file extension of the source file
        (e.g. '.docx')

        source_format: the FileFormat of the source file
        target_format: the FileFormat that the source file should be
        transliterated into
    '''
    def __init__(self, 
        source_path: Path | str, 
        source_format: TextFormat, 
        target_format: TextFormat,
        **kwargs):
        source_path = Path(source_path)

        self.source_path = source_path
        self.source_filename = source_path.name
        self.source_dir = source_path.parent
        self.source_format = source_format
        self.suffix = source_path.suffix
        self.target_format = target_format
        self.target_filename = self.generate_target_filename()
        self.target_dir = kwargs.get('target_dir')
        self.target_path = self.update_target_path(self.target_dir)

        
    def __repr__(self):
        info = f"\
            \nsource path: {str(self.source_path)}\
            \nsource format: {str(self.source_format)}\
            \ntarget format: {str(self.target_format)}\
            \ntarget path: {str(self.target_path)}"
        return info


    def generate_target_filename(self):
        """generates what the filename of the file should be
        """
        target_filename = Path(
            # f"{self.source_path.stem} +
            #                     self.source_format.to_string() +
            #                     ' to ' +
            #                     self.target_format.to_string() +
            #                     ' transliterated' +
            #                     self.source_path.suffix
            )

        return target_filename

    def update_target_path(self, target_dir: Path):
        """updates transliterand to a certain target folder

        Arguments:
            target_folder: a Path to the desired output folder
        """
        if target_dir is None:
            self.target_dir = self.source_dir
        
        self.target_path = Path(self.target_dir / self.target_filename)
    
if __name__ == "__main__":
    __package__ = "hulqcorpustools.resources"
    print(Graphemes().correspondence_dict(
        "orthography", "apaunicode"
    ))