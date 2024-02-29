'''takes a text file and processes it
replacing each line and writing it to file'''

from flashtext import KeywordProcessor
from pathlib import Path

from ...resources.constants import TextFormat, TransliterandFile
from . import replaceengine as repl

def transliterate_txt_wordlist(
    txt_transliterand: Path,
    source_format: TextFormat,
    target_format: TextFormat,
    source_kp: KeywordProcessor,
    eng_kp: KeywordProcessor,
    **kwargs
    ):

    if kwargs.get('outdir'):
        out_dir = kwargs.get('outdir')
    else:
        out_dir = txt_transliterand.parent

    out_filename = f"{txt_transliterand.stem}-{source_format}-to-{target_format}-transliterated.txt"
    out_path = out_dir.joinpath(out_filename)
    with (
        open(txt_transliterand, 'r+') as opened_source_file,
        open(out_path, 'w+') as opened_target_file
    ):

        for line in opened_source_file:
            found_hulq_words = source_kp.extract_keywords(line)
            found_eng_words = eng_kp.extract_keywords(line)

        if len(found_hulq_words) > len(found_eng_words) or len(found_eng_words) == 0:
            transl_line = repl.transliterate_string(line, 
            source_format, 
            target_format)

            opened_target_file.write(line)
            

# TODO: wordlist search for .txt as well

# // if __name__ == "__main__":
