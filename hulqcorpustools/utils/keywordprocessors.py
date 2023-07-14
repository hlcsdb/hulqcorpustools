
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

    def prepare_hulqkeywordprocessor(self, file_format: FileFormat, **kwargs) -> dict:
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
        hulq_wordlist_filename = f'hulq-wordlist-{file_format_name}'
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


    def determine_language_from_text(
        self,
        _text: str,
        **kwargs) -> FileFormat | str:
        """determines which language the line is in

        Arguments:
            _text: the string of text to determine
        Returns:
            the language that has been determined for the line in FileFormat
        Kwargs:
            interactive: if True, prompts user to say which languge the line appears
            to be in
        
        """

        if len(_text.strip()) < 1:
            return None



        language_counter = Counter()
        found_apa_words = self.apa_kp.extract_keywords(_text)
        found_orthog_words = self.orthog_kp.extract_keywords(_text)
        found_english_words = self.eng_kp.extract_keywords(_text)


        language_counter.update({
            FileFormat.APAUNICODE : len(found_apa_words),
            FileFormat.ORTHOGRAPHY: len(found_orthog_words),
            'english': len(found_english_words)
        })
        determined_language = language_counter.most_common(1)

        if determined_language is None:
            return None
        
        else:
            return determined_language[0][0]

        if self.eng_keywordprocessor == None:
            self.eng_keywordprocessor = self.prepare_engkeywordprocessor()

        found_hulq_words = _hulq_kp.extract_keywords(_text)
        found_english_words = _eng_kp.extract_keywords(_text)

        if kwargs.get('verbose') is True:
            print(f'your line: {_text}')
            print(f'{len(found_hulq_words)} hulq words found: {found_hulq_words}')
            print(f'{len(found_english_words)} english words found: {found_english_words}')

        if len(found_hulq_words) == len(found_english_words):

            if kwargs.get('interactive'):
                interactive = True
            else:
                return None


            while interactive is True:
                interactive = input("language not determined: \
                    please input 'e' if it appears to be a line of English, \
                    'h' a line of Hul’q’umi’num’, \
                    or 'u' for undetermined:" + 
                f"hulq words: {found_hulq_words} \n" +
                f"english words: {found_english_words} \n" +
                f"\n{_text}\n")
                if interactive == 'e':
                    found_english_words.append('english')
                elif interactive == 'h':
                    found_hulq_words.append('Hul’q’umi’num’')
                elif interactive == 'u':
                    return True
                else:
                    print('sorry, input not recognized. Trying again...')
                    interactive = True

        if len(found_hulq_words) > len(found_english_words):
            return FileFormat.from_string(_hulq_kp_format)
        if len(found_english_words) > len(found_hulq_words):
            return FileFormat.ENGLISH