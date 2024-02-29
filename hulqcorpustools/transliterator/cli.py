
from pathlib import Path
import sys

from hulqcorpustools.transliterator.transliterator import controller
from hulqcorpustools.resources.constants import TextFormat

def _cli_validate_args(_transliterand_string_or_path: str,
                       _source_format: str,
                       _target_format: str
                       ):
    ...
    try:
        TextFormat.from_string(_target_format)
    except TypeError:
        error = f"Uh oh! Your target format isn't right. You typed {_target_format}. Please check your spelling."
        return error
    try:
        TextFormat.from_string(_source_format)
    except TypeError:
        error = f"Uh oh! Your source format isn't right. You put {_source_format}. Please check your spelling."
        return error

    if Path(_transliterand_string_or_path).exists:
        _cli_transliterate_path(Path(_transliterand_string_or_path), TextFormat.from_string(_source_format), TextFormat.from_string(_target_format))

    
    

    # except Error:    if Path(_transliterand_string_or_path()

def _cli_transliterate_path(_path: Path, _source_format: TextFormat, _target_format: TextFormat):
    ...
    if _path.suffix == 'docx':
        controller.FileController({'docx': [Path(_path)]})
    if _path.suffix == 'txt':
        controller.FileController({'txt': [Path(_path)]})
    # elif Path(_path):
    #     ...

def _cli_transliterate_string(_string: str, _source_format: TextFormat, _target_format: TextFormat):
    """transliterates string at command line

    Arguments:
        _string -- _description_
        _source_format -- _description_
        _target_format -- _description_
    """
    return controller.string_transliterator(_string, TextFormat.from_string(_source_format), TextFormat.from_string(_target_format))

if __name__ == "__main__":
    _transliterand_string_or_path = sys.argv[1]
    
    # print(len(sys.argv))
    # print(sys.argv[0])
    # print(sys.argv[1])
    cool = _cli_validate_args(sys.argv[1], sys.argv[2], sys.argv[3])
    print(cool)
    # print(controller.string_processor('thi', FileFormat.ORTHOGRAPHY, FileFormat.APAUNICODE))
    