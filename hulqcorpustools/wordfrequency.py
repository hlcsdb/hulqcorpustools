
from collections import Counter
import json
from pathlib import Path
import re

from docx import Document as construct_document
from docx.document import Document

from hulqcorpustools.utils.files import FileHandler
from hulqcorpustools.utils.keywordprocessors import HulqKeywordProcessors
from hulqcorpustools.resources.constants import FileFormat
from hulqcorpustools.resources import wordlists

_kp = HulqKeywordProcessors(eng=True)

reg_str_pattern = re.compile(r"[\"\'\!\.\,\?\[\]\(\)\“\”\;]|LH\t|LE\t")


class WordCounter():

    def __init__(self):
        self.total = Counter()

    def count_all_words_in_string(self, _str: str) -> Counter:
        reg_str = re.sub(reg_str_pattern, "", _str)
        count_words = Counter((i for i in reg_str.split()))

        return count_words
    
    def count_all_hulq_words_in_string(self, _str: str) -> Counter:
        count_words_apa = Counter(_kp.apa_kp.extract_keywords(_str))
        count_words_orthog = Counter(_kp.orthog_kp.extract_keywords(_str))

        return max(count_words_apa, count_words_orthog, key=len)
    
    def count_docx_words(self, _docx: Path):
        docx = construct_document(_docx) # type: Document
        for par in docx.paragraphs:
            _reg_text = re.sub(reg_str_pattern, "", par.text)
            _lang = _kp.determine_language_from_text(_reg_text)
            if _lang == FileFormat.APAUNICODE or _lang == FileFormat.ORTHOGRAPHY:
                self.total.update(_reg_text.split())
        for table in docx.tables:
            for row in table.rows:
                for cell in row.cells:
                    for paragraph in cell.paragraphs:
                        for run in paragraph.runs:
                            _reg_text = reg_str_pattern.sub("", run.text)
                            _lang = _kp.determine_language_from_text(_reg_text)
                            if _lang == FileFormat.APAUNICODE or _lang == FileFormat.ORTHOGRAPHY:
                                self.total.update(_reg_text.split())
        return self.total

    def count_txt_words(self, _txt: Path):
        running_counter = Counter()
        with open(_txt) as _txt_file:
            for _line in _txt:
                _reg_text = reg_str_pattern.sub("", _line)
                _lang = _kp.determine_language_from_text(_reg_text)
                if _lang == FileFormat.APAUNICODE or _lang == FileFormat.ORTHOGRAPHY:
                    running_counter.update(_reg_text.split())

        self.total.update(running_counter)

        return running_counter
    
class WordCountFileHandler(FileHandler):

    def __init__(
            self,
            files_list = (list[Path])
        ):
        
        super().__init__(files_list)
        self.counter = WordCounter()
        self.count_all_words_in_files()


    def count_all_words_in_files(self):
        for _file in self.docx_files:
            self.counter.count_docx_words(_file)





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
