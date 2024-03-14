
import sys
from collections import Counter
from collections.abc import Iterable

from hulqcorpustools.resources.wordlists import Wordlist
from hulqcorpustools.resources.graphemes import Graphemes
from hulqcorpustools.resources.constants import TextFormat


class TextCounter():

    def __init__(self,
        text_formats: Iterable[TextFormat],
        wordlists=None,
        graphemes=None,
        eng=False):

        if not wordlists:
            wordlists = {text_format: Wordlist(text_format)
                            for text_format in text_formats}
        
        if not graphemes:
            graphemes = Graphemes(text_formats)

        self.text_formats = text_formats
        self.wordlists = wordlists
        self.graphemes = graphemes

    def count_text_format_words(
        self,
        _text: str,
        _text_format: TextFormat) -> Counter:
        """Count all words in a given text format

        Args:
            _text (str): a multi-word string of text
            _text_format (TextFormat): the text format to check for words

        Returns:
            Counter: the words counted
        """

        _words = (self.graphemes.sanitize(word, _text_format)
            for word in _text.split())

        return Counter(filter(
            lambda x: x in self.wordlists.wordlists.get(_text_format).words, _words))

    def count_all_text_formats(
         self,
         _text: str
         ) -> dict[TextFormat: Counter]:

        found_words = {
            _text_format: 
            self.count_text_format_words(_text, _text_format)
            for _text_format in self.text_formats
        }

        return found_words

    def determine_text_format(
        self,
        _text: str) -> tuple[TextFormat, Counter]:
        """determines which language the line is in
        """
        all_lang_words = self.count_all_text_formats(_text)
        return max(all_lang_words.items(), key=lambda x: x[1].total())

if __name__ == "__main__":
    ...