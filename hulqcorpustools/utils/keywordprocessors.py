
from collections import Counter

from flashtext import KeywordProcessor

from hulqcorpustools.resources.wordlists import Wordlist
from hulqcorpustools.resources.constants import TextFormat, Graphemes, Grapheme


class TextFormatKeywordProcessors():

    def _init_kp(
            text_format: TextFormat
            ):
        """Initialize a KeywordProcessor from a wordlist associated with text format.

        Args:
            text_format (TextFormat): A text format with associated wordlist.

        Returns:
            KeywordProcessor: The KeywordProcessor for that wordlist.
        """
        wordlist = Wordlist(text_format)
        _kp = KeywordProcessor(case_sensitive=True)

        if text_format is not TextFormat.ENGLISH:
            text_format_characters = Graphemes().text_format_graphemes(
                text_format,
                Grapheme("characters")
            )
            _kp.set_non_word_boundaries(
                text_format_characters
                )

        _kp.add_keyword_from_file(wordlist.path)
        return _kp
    
    apa_kp = Wordlist(TextFormat.APAUNICODE).words
    orthog_kp = Wordlist(TextFormat.ORTHOGRAPHY).words # _init_kp(TextFormat.ORTHOGRAPHY)
    straight_kp = Wordlist(TextFormat.STRAIGHT).words
    eng_kp = Wordlist(TextFormat.ENGLISH).words
    # eng_kp = _init_kp(TextFormat.ENGLISH)

    def get_all_lang_words(
            self,
            _text: str
            ) -> dict[TextFormat: list[str]]:

        found_straight_words = Counter(map(lambda x: x in self.straight_kp, _text.split()))
        found_apa_words = Counter(map(lambda x: x in self.apa_kp, _text.split()))
        found_orthog_words = Counter(map(lambda x: x in self.orthog_kp, _text.split())) # self.orthog_kp.extract_keywords(_text)
        found_english_words = Counter(map(lambda x: x in self.eng_kp, _text.split()))

        found_words = {
            TextFormat.STRAIGHT: found_straight_words,
            TextFormat.APAUNICODE: found_apa_words,
            TextFormat.ORTHOGRAPHY: found_orthog_words,
            TextFormat.ENGLISH: found_english_words
            }

        return found_words

    def count_lang_words(
            self,
            found_words: dict
            ) -> tuple[Counter, dict]:

        language_counter = Counter()

        language_counter.update({
            language_found[0]: len(language_found[1])
            for language_found in found_words.items()
        })
        return language_counter

    def determine_text_format(
        self,
        _text: str) -> TextFormat:
        """determines which language the line is in
        """

        all_lang_words = self.get_all_lang_words(_text)
        language_counter = self.count_lang_words(all_lang_words)

        determined_language = language_counter.most_common(1)[0][0]

        return TextFormat(determined_language)


kp = TextFormatKeywordProcessors()
