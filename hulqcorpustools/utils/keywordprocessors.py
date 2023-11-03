
from collections import Counter

from flashtext import KeywordProcessor

from hulqcorpustools.resources.wordlists import wordlist_paths
from hulqcorpustools.resources.constants import FileFormat, GraphemesDict

class HulqKeywordProcessors():

    def __init__(self,
                 **kwargs
                ):

        self.apa_kp = self.prepare_hulqkeywordprocessor(FileFormat.APAUNICODE)
        self.orthog_kp = self.prepare_hulqkeywordprocessor(FileFormat.ORTHOGRAPHY)
        self.straight_kp = self.prepare_hulqkeywordprocessor(FileFormat.STRAIGHT)



        if kwargs.get('eng') == True:
            self.eng_kp = self.prepare_engkeywordprocessor()

    def get_kp(self, file_format: FileFormat):
        """get a KeywordProcessor based on file_format"""

        if file_format == FileFormat.APAUNICODE:
            return self.apa_kp
        if file_format == FileFormat.ORTHOGRAPHY:
            return self.orthog_kp
        if file_format == FileFormat.STRAIGHT:
            return self.straight_kp


    def prepare_hulqkeywordprocessor(self, file_format: FileFormat, **kwargs) -> KeywordProcessor:
        """prepare a KeywordProcessor from a wordlist determined by FileFormat

        Arguments:
            source_format -- the source format to be transliterated
        Kwargs:
            --update-wordlist: opens the other format wordlists if they are supposed to be
            updated
        """

        def get_non_word_boundary_chars(file_format: FileFormat):
            """gets all of the characters that might not be in [a-zA-Z] or whatever

            Arguments:
                text_format -- a FileFormat of some source
            """
            non_word_boundary_chars = (i for i in GraphemesDict(file_format).source_format_characters)
            return non_word_boundary_chars

        file_format_name = file_format.to_string()
        hulq_wordlist_filename = f'hulq-wordlist-{file_format_name}'.casefold()
        hulq_wordlist_filepath = wordlist_paths.get(hulq_wordlist_filename)

        hulq_keywordprocessor = KeywordProcessor()
        hulq_keywordprocessor.set_non_word_boundaries(get_non_word_boundary_chars(file_format))
        hulq_keywordprocessor.add_keyword_from_file(hulq_wordlist_filepath)
        return hulq_keywordprocessor

    def prepare_engkeywordprocessor(self):
        eng_wordlist_filepath = wordlist_paths.get("words_alpha_vowels_longer_words")

        eng_keywordprocessor = KeywordProcessor()
        eng_keywordprocessor.add_keyword_from_file(eng_wordlist_filepath)

        return eng_keywordprocessor

    def get_all_lang_words(
            self,
            _text: str) -> dict[FileFormat: list[str]]:
        
        found_straight_words = self.straight_kp.extract_keywords(_text)
        found_apa_words = self.apa_kp.extract_keywords(_text)
        found_orthog_words = self.orthog_kp.extract_keywords(_text)
        found_english_words = self.eng_kp.extract_keywords(_text)

        found_words = {
            FileFormat.STRAIGHT: found_straight_words,
            FileFormat.APAUNICODE: found_apa_words,
            FileFormat.ORTHOGRAPHY: found_orthog_words,
            FileFormat.ENGLISH: found_english_words
            }
        
        return found_words

    def count_lang_words(
            self,
            found_words: dict
        ) -> (Counter, dict):

        language_counter = Counter()

        language_counter.update({
            language_found[0]: len(language_found[1]) for language_found in found_words.items()
        })
        return language_counter



    def determine_language_from_text(
        self,
        _text: str,
        **kwargs) -> FileFormat | str:
        """determines which language the line is in
        """

        all_lang_words = self.get_all_lang_words(_text)
        language_counter = self.count_lang_words(all_lang_words)

        determined_language = language_counter.most_common(1)[0][0]

        return determined_language