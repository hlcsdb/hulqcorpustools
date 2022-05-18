'''
opens up keywordprocessor wordlists and tells you whether a string of text is in orthography, APA unicode, straight, English, or none based on comparing to wordlist
'''
from flashtext import KeywordProcessor
from pathlib import Path

from hulqcorpusresources import constants
from hulqcorpusresources.graphemes import loaded_graphemes
from hulqcorpusresources.wordlists import wordlist_paths

for i in constants.FileFormat.file_formats():
    print(i)

# hulq_apa_wordlist_path = wordlist_paths['hulq-wordlist-APAUnicode.txt']
# hulq_apa_keywordprocessor = KeywordProcessor()
# hulq_apa_keywordprocessor.add_keyword_from_file(hulq_apa_wordlist_path)

# hulq_straight