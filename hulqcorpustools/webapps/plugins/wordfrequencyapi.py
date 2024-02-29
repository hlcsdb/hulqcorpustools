
from collections import Counter
from pathlib import Path

from hulqcorpustools.wordfrequency import WordCounter, WordCountFileHandler
from werkzeug.datastructures import FileStorage

def string_word_count(input_text: str) -> Counter:
    _word_counter = WordCounter()
    _word_count = _word_counter.count_all_hulq_words_in_string(input_text).most_common()

    return _word_count

def file_word_count(_files: list[FileStorage]) -> Counter:
    _file_counter = WordCountFileHandler(_files)
    _word_count = _file_counter.counter.total.most_common()
    return _word_count
