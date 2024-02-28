
from collections import Counter

from flashtext import KeywordProcessor

from hulqcorpustools.resources.wordlists import wordlist_paths
from hulqcorpustools.resources.constants import TextFormat, Graphemes, Grapheme


class HulqKeywordProcessors():

    def _init_kp(
            text_format: TextFormat
            ) -> KeywordProcessor:
        """Initialize a KeywordProcessor from a wordlist associated with text format.

        Args:
            text_format (TextFormat): A text format with associated wordlist.

        Returns:
            KeywordProcessor: The KeywordProcessor for that wordlist.
        """
        text_format_wordlist_name = f"hulq-wordlist-{text_format}"
        wordlist_path = wordlist_paths.get(text_format_wordlist_name)
        text_format_characters = Graphemes().text_format_graphemes(
            text_format, Grapheme("characters")
        )

        hulq_keywordprocessor = KeywordProcessor()
        hulq_keywordprocessor.set_non_word_boundaries(
            text_format_characters
            )

        hulq_keywordprocessor.add_keyword_from_file(wordlist_path)
        return hulq_keywordprocessor

    def _init_eng_kp() -> KeywordProcessor:
        """Initialize English keyword processor.

        Returns:
            KeywordProcessor: The KeywordProcessor for the English wordlist.
        """
        eng_wordlist_filepath = wordlist_paths.get(
            "words_alpha_vowels_longer_words"
            )

        eng_keywordprocessor = KeywordProcessor()
        eng_keywordprocessor.add_keyword_from_file(eng_wordlist_filepath)

        return eng_keywordprocessor

    apa_kp = _init_kp(TextFormat.APAUNICODE)
    orthog_kp = _init_kp(TextFormat.ORTHOGRAPHY)
    straight_kp = _init_kp(TextFormat.STRAIGHT)
    eng_kp = _init_eng_kp()

    def get_kp(self, file_format: TextFormat):
        """get a KeywordProcessor based on file_format"""

        if file_format == TextFormat.APAUNICODE:
            return self.apa_kp
        if file_format == TextFormat.ORTHOGRAPHY:
            return self.orthog_kp
        if file_format == TextFormat.STRAIGHT:
            return self.straight_kp

    def get_all_lang_words(
            self,
            _text: str
            ) -> dict[TextFormat: list[str]]:

        found_straight_words = self.straight_kp.extract_keywords(_text)
        found_apa_words = self.apa_kp.extract_keywords(_text)
        found_orthog_words = self.orthog_kp.extract_keywords(_text)
        found_english_words = self.eng_kp.extract_keywords(_text)

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

    def determine_language_from_text(
        self,
        _text: str) -> TextFormat | str:
        """determines which language the line is in
        """

        all_lang_words = self.get_all_lang_words(_text)
        language_counter = self.count_lang_words(all_lang_words)

        determined_language = language_counter.most_common(1)[0][0]

        return determined_language