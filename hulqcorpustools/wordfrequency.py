
from collections import Counter
import json
from pathlib import Path
import re

from docx import Document as construct_document
from docx.document import Document

from hulqcorpustools.utils.keywordprocessors import HulqKeywordProcessors
from hulqcorpustools.resources.constants import FileFormat
from hulqcorpustools.resources import wordlists

_kp = HulqKeywordProcessors(eng=True)

reg_str_pattern = re.compile(r"[\"\'\!\.\,\?\[\]\(\)\“\”\;]|LH\t|LE\t")

class WordCounter():

    def __init__(self):
        self.kp = HulqKeywordProcessors()

    def count_all_words_in_string(self, _str: str) -> Counter:
        reg_str = re.sub(reg_str_pattern, "", _str)
        count_words = Counter((i for i in reg_str.split()))

        return count_words
    
    def count_all_hulq_words_in_string(self, _str: str) -> Counter:
        count_words_apa = Counter(self.kp.apa_kp.extract_keywords(_str))
        count_words_orthog = Counter(self.kp.orthog_kp.extract_keywords(_str))

        return max(count_words_apa, count_words_orthog, key=len)
    
    def count_all_words_in_docx(self, _docx: Path):
        running_counter = Counter()
        docx = construct_document(_docx)
        for par in docx.paragraphs:
            reg_par_text = re.sub(reg_str_pattern, "", par.text)
            line_language = _kp.determine_language_from_text(reg_par_text)
            if line_language == FileFormat.APAUNICODE or line_language == FileFormat.ORTHOGRAPHY:
                running_counter.update(reg_par_text.split())

        return running_counter

def write_frequency_to_txt(output_filepath: Path, counted_words: Counter):
    """writes the result of counting word frequency to a txt file

    Arguments:
        output_filepath -- path to the output file
        counted_words -- output of the counted_words fn
    """
    with open(output_filepath, 'w+') as output_file:
        for i in counted_words.most_common():
            output_file.write(i[0] + '\t' + str(i[1]) + '\n')

def write_frequency_to_json(output_filepath: Path, counted_words: Counter):
    """writes the reuslt of counting word frequency to a json

    Arguments:
        output_filepath -- path to the output file
        counted_words -- output of the counted_words fn
    """
    with open(output_filepath, 'w+') as open_file:
        json.dump(dict(counted_words.most_common()), open_file, ensure_ascii=False, indent=0)
