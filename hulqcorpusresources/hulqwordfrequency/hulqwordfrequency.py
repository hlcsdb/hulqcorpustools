from collections import Counter
from .. import wordlists
from pathlib import Path
import regex as re

text_corpus = Path(__file__).resolve().parent / 'data' / 'Texts-corpus-ZG8.txt'
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
    """

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
                    if word == 'LH' or is_number.fullmatch(word):
                        continue
                    elif words.get(word):
                        words[word] += 1
                    else:
                        words.update({word:1})
                
                line_count += 1

            if line_count == line_limit:
                return words
            
        return words

def write_frequency_to_txt(output_filepath: Path, counted_words: list[tuple]):
    """_summary_

    Arguments:
        output_filepath -- path to the output file
        counted_words -- output of the counted_words fn
    """
    
    with open(output_filepath, 'w+') as output_file:
        for i in counted_words.most_common():
            output_file.write(i[0] + '\t' + str(i[1]) + '\n')

def open_hukari_peter_wordlist_from_df():
    return wl.HulqWordlists.hukari_peter_xlsx_df

if __name__ == "__main__":

    print(wl.HulqWordlists)
    # cool = open_hukari_peter_wordlist_from_df()
    