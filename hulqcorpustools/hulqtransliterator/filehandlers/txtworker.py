'''takes a text file and processes it
replacing each line and writing it to file'''

from flashtext import KeywordProcessor
from pathlib import Path

from ...resources.constants import FileFormat, TransliterandFile
from ..transliterator import replaceengine as repl


def transliterate_txt(
    transliterand: TransliterandFile
    ):
    """transliterate the given .txt file
    args:
        transliterand: the TransliterandFile.txt file to transliterate
        
        opens file, goes through each line, writes transliterated line
        to new file
    """
    with (
        open((transliterand.source_path), 'r+') as opened_source_file,
        open((transliterand.target_path), 'w+') as opened_target_file):

        for i in opened_source_file:
            newi = repl.transliterate_string_replace(i, 
            transliterand.source_format, 
            transliterand.target_format)
            opened_target_file.write(newi)


def transliterate_txt_wordlist(
    transliterand: TransliterandFile,
    source_kp: KeywordProcessor,
    eng_kp: KeywordProcessor,
    **kwargs
    ):
    """_summary_

    Arguments:
        transliterand -- _description_
        keyword_processors -- _description_
    """
    with (
        open((transliterand.source_path), 'r+') as opened_source_file,
        open((transliterand.target_path), 'w+') as opened_target_file):

        for i in opened_source_file:
            found_hulq_words = source_kp.extract_keywords(i)
            found_eng_words = eng_kp.extract_keywords(i)

        if len(i) > len(found_eng_words) or len(found_eng_words) == 0:
            newi = repl.transliterate_string_replace(i, 
            transliterand.source_format, 
            transliterand.target_format)
            opened_target_file.write(newi)
            

# TODO: wordlist search for .txt as well

# // if __name__ == "__main__":
