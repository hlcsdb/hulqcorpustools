from enum import Enum, auto
import json
import os
from pathlib import Path
from hulqcorpustools.resources.graphemes import loaded_graphemes

class FileFormat(Enum):
    """possible text formats for a doc to be in

        'Straight': only as a source file, kludge characters for use with the
        Straight font
        'orthography': practical orthography written with conventional
        keyboard characters 
        'APAUnicode': APA (Americanist Phonetic Alphabet) written with Unicode
        characters

        Functions:
            file_formats: returns the set of FileFormats
            (e.g. for excluding FileFormats for some operations)
            from_string: returns a FileFormat from text
                Arguments: a string representaiton of a FileFormat
            to_string: returns the string representation of a FileFormat
                Arguments: a FileFormat
        

    
    """

    STRAIGHT = auto()
    APAUNICODE = auto()
    ORTHOGRAPHY = auto()

    @staticmethod
    def file_formats():
        file_formats = {FileFormat.STRAIGHT, FileFormat.APAUNICODE, FileFormat.ORTHOGRAPHY}
        return file_formats

    @classmethod
    def from_string(cls, *args):
        '''in case the value gets turned to a string-- 
        turn it back to this class'''

        args = [i.casefold().replace(' ', '') for i in args]

        if 'straight'.casefold() in args or 'fileformat.straight'.casefold() in args:
            cls = FileFormat.STRAIGHT
        elif 'apaunicode'.casefold() in args or 'fileformat.apaunicode'.casefold() in args:
            cls = FileFormat.APAUNICODE
        elif 'orthography'.casefold() in args or 'fileformat.orthography'.casefold() in args:
            cls = FileFormat.ORTHOGRAPHY

        return cls

    def to_string(self):
        if self == FileFormat.APAUNICODE:
            file_format_str = 'APAUnicode'
        else:
            file_format_str = self.name.lower()

        return file_format_str

class GraphemesDict(dict):
    """a dict of graphemes or correspondending graphemes for
    hul’q’umi’num’

    Attributes:
        source_format: a FileFormat of the source format for some
        correspondences
        source_format_str: the string representation of the source format
        (i.e. its name)
        source_format_lemmas: a dict with all of the 'correct'
        representations of the character in the source format
        source_format_characters: a dict with all representations
        of the character in the source format

        (optional attributes follow)
        target_format: a FileFormat of the target format for
        correspondencess
        target_format_str: the string representaiton of the target format
        (i.e. its name)
        target_format: a dict with all of the 'correct'
        representations of the character in the target format
        target_format_characters: a dict with all representations
        of the character in the target format

        correspondence_dict: a dict of form 
        {{source format lemma i:target format lemma i}, ...} for some 
        corresponding graphemes
    """
    def __init__(self, source_format: FileFormat, *args):
        """
        Arguments:
            source_format -- a FileFormat of a source format
        Optional arguments:
            target_format -- a FileFormat of the target format
            for finding grapheme correspondences
        """
        self.source_format = source_format
        self.source_format_str = source_format.to_string()

        if self.source_format is FileFormat.STRAIGHT:
            self.source_format_lemmas = None
        else:
            self.source_format_lemmas = {
                i[self.source_format_str]['Lemma'] for i in loaded_graphemes
                }
        self.source_format_characters = {
            i[self.source_format_str]['Characters'] for i in loaded_graphemes
            }

        # if you include as second argument for the target form: 
        # turn those into dicts and make correspondence dict
        if args:
            self.target_format = args[0]
            self.target_format_str = self.target_format.to_string()
            self.target_format_characters = {
                i[self.target_format_str]['Characters'] for i in loaded_graphemes}
            self.target_format_lemmas = {
                i[self.target_format_str]['Lemma'] for i in loaded_graphemes}
            self.correspondence_dict = {
                i[self.source_format_str]['Lemma']:i[self.target_format_str]['Characters']
                for i in loaded_graphemes}
        
        
        else:
            self.target_format = None
            self.target_format_str = None
            self.target_format_characters = None
            self.correspondence_dict = self.source_format_lemmas

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
    source_format: FileFormat, 
    target_format: FileFormat,
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
        info = ''.join([
            '\nsource path: ', str(self.source_path),
            '\nsource format: ', str(self.source_format),
            '\ntarget format: ', str(self.target_format),
            '\ntarget path: ', str(self.target_path)])
        return info


    def generate_target_filename(self):
        """generates what the filename of the file should be
        """
        target_filename = Path(self.source_path.stem + 
                                ' ' +
                                self.source_format.to_string() +
                                ' to ' +
                                self.target_format.to_string() +
                                ' transliterated' +
                                self.source_path.suffix)

        return target_filename

    def update_target_path(self, target_dir: Path):
        """updates transliterand to a certain target folder

        Arguments:
            target_folder: a Path to the desired output folder
        """
        if target_dir is None:
            self.target_dir = self.source_dir
        
        self.target_path = Path(self.target_dir / self.target_filename)

        return(self.target_path)
    
if __name__ == "__main__":
    # print(loaded_graphemes)
    ...