'''
engine for replacing characters in one orthography of Hul’q’umi’num’
with another
'''

import regex as re
from ...resources.constants import FileFormat, GraphemesDict

def transliterate_string_replace(
    linestring,
    source_format: FileFormat,
    target_format: FileFormat) -> str:
    '''    find all instances of a substring and replaces them in place
    
    copied from somewhere on Stack Overflow... don't remember where...
    thank you to whoever is out there...

    

    Arguments:
        linestring -- the transliterand string
        source_format -- the source format to be transliterated from
        target_format -- the target to be transliterated into

    Returns:
        the transliterated string
    '''

    # make a replacement dictionary out of the requested formats,
    # sort, then turn it to a long regex

    working_dict = GraphemesDict(source_format, target_format).correspondence_dict
    substrings = sorted(working_dict, key=len, reverse=True)
    print(substrings)
    regexp = re.compile('|'.join(map(re.escape, substrings)))
    
    if source_format == FileFormat.ORTHOGRAPHY:
        linestring = glottalized_resonant_reverter(linestring)

    transliterated_line = regexp.sub(
        lambda match: working_dict[match.group(0)], linestring)

    if target_format == FileFormat.ORTHOGRAPHY:
        transliterated_line = glottalized_resonant_mover(transliterated_line)

    return transliterated_line
    
def glottalized_resonant_mover(linestring):
    """
    moves glottal character over according to glottalized resonant 
    hierarchy:

    case description: VR’W for some vowels V, W; some glottalized 
    resonant R’

    hierarchy: e > i > a > u
               3 > 2 > 1 > 0

    if h(V) > h(W), then string is V’RW
    
    """

    hi_scores = {'e' : 3,
                'i' : 2,
                'a' : 1,
                'u' : 0}

    def hierarchy_sub(matchobj):
        """moves glottalized resonant if a vowel pulls it one way
        or the other
        """

        if hi_scores[matchobj.group(1)] > hi_scores[matchobj.group(4)]:

            swap_string = ''.join(
                [
                matchobj.group(1),
                matchobj.group(3),
                matchobj.group(2),
                # // matchobj.group(4)
                ]
            )
            return swap_string

        else:
            return matchobj.group(0)

    glot_res_re = re.compile('(a|e|i|u)(l|m|n|w|y)(’)(?=(a|e|i|u))')
    swapstring = glot_res_re.sub(hierarchy_sub, linestring)
    
    return swapstring

def glottalized_resonant_reverter(linestring):
    """when going from orthography to APA -- move glottal stop back to
    following glottalized resonant so it is recognized"""

    glot_res_revert_re = re.compile('(’)(l|m|n|w|y)')
    swapstring_revert = glot_res_revert_re.sub(r'\2\1', linestring)

    return swapstring_revert


if __name__ == "__main__":
    test_string = '’i ’u ch ’uy’ ’ul’'
    tested = transliterate_string_replace(test_string, FileFormat.ORTHOGRAPHY, FileFormat.APAUNICODE)
    print(tested)