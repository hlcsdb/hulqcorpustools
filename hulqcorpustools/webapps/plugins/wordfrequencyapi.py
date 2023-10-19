
from collections import Counter
from hulqcorpustools import wordfrequency

def get_word_frequency_text(_input_text: str):
    print(_input_text)
    _word_counter = wordfrequency.WordCounter()
    count = _word_counter.count_all_words_in_string(_input_text) # type: Counter

    return format_return_counts(count)

def get_word_frequency_file(file_to_count):
    
    _word_counter = wordfrequency.WordCounter()
    count = _word_counter.count_all_words_in_docx(file_to_count)
    return format_return_counts(count) 

def format_return_counts(word_count: Counter):
    sorted_count = word_count.most_common()
    sorted_count_str = '\n'.join([f'{counted_word[1]}\t{counted_word[0]}' for counted_word in sorted_count])
    return sorted_count_str