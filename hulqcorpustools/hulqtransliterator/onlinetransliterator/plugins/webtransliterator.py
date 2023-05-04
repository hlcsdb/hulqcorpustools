from ... import transliterator
from ....resources.constants import FileFormat

def web_transliterate_string(hulq_string: str,
                            source_format = (FileFormat | str),
                            target_format = (FileFormat | str)):

    if type(source_format) == str:
        source_format = FileFormat.from_string(source_format)
        
    if type(target_format) == str:
        target_format = FileFormat.from_string(target_format)
        
    
    return transliterator.controller.string_processor(hulq_string, source_format, target_format)
