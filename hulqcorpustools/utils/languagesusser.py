
from flashtext import KeywordProcessor as kp

from ..resources.constants import FileFormat
from ..resources.wordlists import Wordlist

def _load_flashtext(
    _wordlist_format: None | str
    ):
    """Load the wordlists used by flashtext to determine which language a
    string of text is in
    
    If the language susser is called, then the flashtext keyword processors must
    be loaded

    Arguments:
        _wordlist_format -- the format (e.g. English, orthography, or APA) 
        of the wordlist to be loaded

    Returns:
        a 
    """


    if _wordlist_format is None:
        _wordlist = Wordlist.ORTHOGRAPHY_WORDLIST_TEXT

    else:
        _wordlist = Wordlist.load_wordlist_text(_wordlist_format)

    _wordlist = _wordlist.split()

    _hulq_kp = kp()
    _hulq_kp.add_non_word_boundary('’')
    _hulq_kp.add_keywords_from_list(
        _wordlist
            )

    return _hulq_kp

_hulq_kp_format = "orthography"
_hulq_kp = _load_flashtext(_hulq_kp_format)
_eng_kp = _load_flashtext("english")

def determine_language_from_text(
    _text: str, **kwargs) -> FileFormat:
    """determines which language the line is in

    Arguments:
        _text: the string of text to determine
    Returns:
        the language that has been determined for the line in FileFormat
    Kwargs:
        verbose: if True, prints the string, number of found words,
        which words were found
        interactive: if True, prompts user to say which languge the line appears
        to be in
    
    """

    if len(_text.strip()) < 1:
        return None

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