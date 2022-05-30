from collections import Counter
from flashtext import KeywordProcessor as kp
import json
import pandas as pd
from pathlib import Path
import regex as re

import hwordlists as hw

# paths
text_corpus = Path(__file__).resolve().parent / 'corpus' /  'Texts-corpus-ZG8.txt'
word_frequency_wordlist_path = Path(Path(__file__).resolve().parent / 'hulqwordfrequency/output/word_frequency_wordlist_incl.json')

# regular expression patterns
hulqletters = re.compile(r'a-zA-Z’')
rl = re.compile('([aeiou][\.|\-]){2,}')
strip_punctuation = re.compile('[\.|,|?|“|"|”|\[|\]|1|2|3|4|5|6|7|8|9|0|\(|\)]')
is_number = re.compile('[0-9]+')

def strip_rl_and_punc(word: str) -> str:
    '''strips off rhetorical lengthening (if any) and extraneous punctuation'''

    word_sub = lambda x: strip_punctuation.sub('', rl.sub(r'\1', x))
    
    if len(word_sub(word)) == 0:
        return(word)

    
    return(word_sub(word))

def count_corpus(open_file: Path, **kwargs) -> Counter:
    """counts the incidence of each word in the corpus

    Arguments:
        open_file -- path to the corpus

    kwargs:
        number_of_lines -- the number of lines to consider; this is to limit number of calls (for testing purposes)
        wordlist: Boolean -- if true, summon a keywordprocessor wordlist and check
        whether each word is in the wordlist
    """

    # if the count is to be checked against the wordlist, initialize to check    
    if kwargs.get('wordlist'):
        wordlist_flag = True
        wordlist_keywordprocessor = kp()
        wordlist_keywordprocessor.add_non_word_boundary('’')
        # for now: the wordlist is just the hp one
        wordlist_keywordprocessor.add_keywords_from_list(
            [i.strip() for i in hukari_peter_wordlist_from_df()]
            )
    else:
        wordlist_flag = False
        wordlist_keywordprocessor = []
    
    with open(text_corpus, 'r') as open_file:
        words = Counter()
        # counting a couple for testing purposes
        line_limit = kwargs.get('line_limit')

        # why did i do this at 2
        line_count = 2
        
        for line in open_file:
            if line[0:2] == 'LH':
                line_list = line.split()

                line_list = [strip_rl_and_punc(word) for word in line.split()]
                # skip 'LH' and line number
                for word in line_list:
                    if word == 'LH' or \
                    is_number.fullmatch(word) or \
                    (wordlist_flag == True and word not in wordlist_keywordprocessor):
                        continue
                    elif words.get(word):
                        words[word] += 1
                    else:
                        words.update({word:1})
                
                line_count += 1

            if line_count == line_limit:
                return words
            
        return words

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

def hukari_peter_wordlist_from_df():
    """just gets the wordlist from the df"""
    return hw.HulqWordlists.hukari_peter_xlsx_df.get('LEXEME - curly ’unuhw')

def add_wordlist_to_frequency_list(
    corpus_count: Counter,
    wordlist: pd.DataFrame) -> Counter:
    """takes the counted corpus and adds everything from the established wordlist
    to it, so if it's in the corpus, it's counted, but if it's in the wordlist,
    it just gets a value of 1

    Arguments:
        corpus_count -- a Counter output from corpus_count fn
        wordlist -- the pandas df of the excel wordlist

    Returns:
        changed corpus_count
    """
    corpus_count.update((i.strip() for i in wordlist))

def build_frequency_json(text_corpus_path: Path, word_frequency_wordlist_path: Path):
    """builds the frequency json

    Arguments:
        text_corpus -- path to text corpus
    """
    corpus_count = count_corpus(text_corpus_path, wordlist=True)
    add_wordlist_to_frequency_list(corpus_count, hukari_peter_wordlist_from_df())

    #json output assumed to be in the same place as the wordlist
    json_output_path = word_frequency_wordlist_path
    write_frequency_to_json(corpus_count, json_output_path)

if __name__ == "__main__":
    build_frequency_json(text_corpus, word_frequency_wordlist_path)