'''
takes either a .doc or .docx file and transliterates based on font
or style

in a .docx file, it currently searches by any instances of specific fonts
when it's straight, the font is just Straight
otherwise, it's whatever the user sets-- could just be Times New Roman if
they've gone through their doc and changed everything they need transliterated 
to TNR, but it defaults to BC Sans.

TODO: write real tests and write test checking
    - for each file format to another
'''


from docx import Document
from docx.text import paragraph, run
from flashtext import KeywordProcessor
from pathlib import Path
import os

from ...resources.constants import FileFormat, GraphemesDict, TransliterandFile
from ..transliterator import replaceengine as repl

def transliterate_docx_font(
    transliterand: TransliterandFile, 
    **kwargs):
    '''transliterated a docx file from source format to target format

    Arguments:
        source_path -- the source file to be transliterated
        target_file -- _description_
        source_format -- _description_
        target_format -- _description_

    Returns:
        _description_
    '''

    
    def doc_processor(transliterand: TransliterandFile, **kwargs):

        ''' when source format is straight, procedure for
        transliterating straight
        '''
        # non_hulq = re.compile(r'\.|\s')
 
        # decide which font to search by
        font = kwargs.get('font')
        if transliterand.source_format == FileFormat.STRAIGHT:
            font = 'Straight'
        elif font is None:
            font = 'BC Sans'

        # these are BALONEY!!
        def paragraph_run_concatenator(par: paragraph.Paragraph):
            '''sometimes consecutive runs are part of the same word.
            This fn concatenates the text of those runs 
            r_1, r_2, ... r_n, deletes text up to r_n-1, and plops
            the transliterated text into r_n
            
            so e.g. ['s', 'ts', '’', 'ee', 'l', 'h', 'tun’']
            for text in consecutive runs in one paragraph
            all with the same font (notice they all make one word)
            becomes 'sts’eelhtun’

            this was so annoying to fix... word should be destroyed
            
            Is this un-Pythonic? Maybe. Does it work? Maybe.'''

            # enumerate all of the runs, as we're going to be looking for
            # adjacency of same-font runs
            enumerated_runs = enumerate(par.runs)

            # list of all the consecutive run sequences in a given par
            consecutive_run_sequences = []

            # current list of indices of consecutive runs
            # will result to be e.g. (1, 2, 3, 4)
            consecutive_index = []
            for index, par_run in enumerated_runs:
                par_run: run.Run

                # if a given run happens to be in the searched font,
                # let's add it to our list of indices
                if par_run.font.name == font:

                    # initial index
                    # [0]
                    if len(consecutive_index) == 0:
                        consecutive_index.append(index)
                        continue

                    # for the next run with the right font:
                    # if the index is immediately preceding, then add this run
                    # [0, 1]
                    elif index - 1 in consecutive_index:
                        consecutive_index.append(index)
                        continue

                    # if in the next run in the right font is NOT immediately 
                    # succeeding, then close off that list into a tuple,
                    # file it away, and start a new one
                    # e.g. [0, 1, 2, 3] <-- 6
                    # > consecutive_run_sequences = [(0, 1, 2, 3)]
                    # > consecutive_index = [6]
                    elif index -1 not in consecutive_index:
                        consecutive_tuple = tuple(consecutive_index)
                        consecutive_run_sequences.append(consecutive_tuple)
                        consecutive_index = []
                        continue
            else:
                # if you encounter something NOT in the right font, then
                # you've (presumably) finished off your word, so close off your
                # list to tuple and put it in the consecutive run sequences 
                # list to be transliterated
                if consecutive_index:
                    consecutive_run_sequences.append(tuple(consecutive_index))

                # for each run, concatenate all of the strings (run.text)
                # in each run and transliterate it
                for run_sequence in consecutive_run_sequences:
                    concat_list = [i.text for i in par.runs[min(run_sequence):(max(run_sequence)+1)]]
                    concat_str = ''.join(concat_list)
                    concat_str =  repl.transliterate_string_replace(
                                            concat_str,
                                            source_format,
                                            target_format
                    )

                    
                    for run_index in run_sequence:
                        
                        # delete the text in all of the runs 
                        # that aren't the last
                        if run_index < max(run_sequence):
                            par.runs[run_index].text = ''
                        
                        # change the text in the last run to the 
                        # transliterated string
                        else:
                            par.runs[run_index].text = concat_str

            # TADA
            return par

        def paragraph_font_processor(par: paragraph.Paragraph):
            ''' processes paragraphs based on searching for font'''
            # go through entire paragraphs set to font in question
            if par.style.font.name == font:
                par.text = repl.transliterate_string_replace(
                                par.text,
                                source_format,
                                target_format
                            )

            
            elif (len(par.runs) > 0 and par.style.font.name != font):
                par = paragraph_run_concatenator(par)
            return par

        # turn the doc into a Document, then process each paragraph
        document = Document(transliterand.source_path)
        source_format = transliterand.source_format
        target_format = transliterand.target_format
        for par in document.paragraphs:
            par = paragraph_font_processor(par)

        return document




    _font = kwargs.get('font', None)
    
    transliterated = doc_processor(
                        transliterand, 
                        font=_font
                    )
    transliterated.save(transliterand.target_path)        
    
def transliterate_docx_wordlist(
    transliterand: TransliterandFile,
    source_kp = KeywordProcessor,
    eng_kp = KeywordProcessor,
    **kwargs):
    '''transliterates an entire docx file by wordlist

    Arguments:
        transliterand: a TransliterandFile with the parameters
        keywordprocessors: a dict of all the loaded
        keyword processors
        
    
    Keyword arguments:
        update_wordlist -- include this if you want to update the wordlist
                           with words found in the transliterated lines
    '''

    document = Document(transliterand.source_path)


    for par in document.paragraphs:
        par_text = par.text    
        found_hulq_words = source_kp.extract_keywords(par_text)
        found_eng_words = eng_kp.extract_keywords(par_text)

        # if there is more hulq than there is English -- replace
        if len(found_hulq_words) > len(found_eng_words) or len(found_eng_words) == 0:
            par_text = repl.transliterate_string_replace(
                par.text,
                transliterand.source_format,
                transliterand.target_format
            )
            par.text = par_text
        
        if kwargs.get('update-wordlist') is True:
            update_new_wordlist(
                transliterand.source_format,
                source_kp,
                found_hulq_words)
            if len(found_hulq_words) > 2:
                source_kp.add_keywords_from_list(par_text.replace('.','').split())

    document.save(transliterand.target_path)
    return transliterand.target_path

    # TODO: make a running list of new words to put in the new_wordlist
    # it will be more efficient probably to bring the wordlist in
    # get the difference set ({a, b, c}, {b, c, d} = {d}) and write
    # the difference set to the end of the file
    # TODO: transliterate wordlist into each orthography
    # TODO: clean it up nice (wrote this down and don't remember what it means)



def update_new_wordlist(
    source_format: FileFormat,
    current_keywordprocessor: KeywordProcessor,
    new_keywords: list,
    keywordprocessors_dict: dict):
    """update the running wordlist with things that were transliterated

    Arguments:
        source_format -- the current source format (to get base wordlist folder)
        current_keywordprocessor -- the current keyword processor (to get the keywords)
        new_keywords -- all the found 
    """
    working_wordlist_filepath = Path(__file__).parent / ('resources/wordlists/new-hulq-wordlist-' +
                                                    source_format.to_string() +
                                                        '.txt')

    current_keywords = current_keywordprocessor.get_all_keywords()
    
    set(new_keywords.get_all_keywords().keys())

if __name__ == "__main__":



        # for i in source_list:
        #     target_path = i.with_name(i.stem + 'transliterated').with_suffix('.docx')

        #     transliterate_docx_wordlist(
        #         i,
        #         target_path,
        #         source_format,
        #         target_format,
        #     )




    def test_unicode_ortho():
        ''' little unit test ... change it if other things are needed'''
        source_format = FileFormat.APAUNICODE
        target_format = FileFormat.ORTHOGRAPHY
        ### put a test file here
        source_file_name = Path('./tests/docx')
        target_path = source_file_name.with_name(source_file_name.stem + 'transliterated').with_suffix('.docx')
        font = 'Tahoma'

        transliterate_docx_font(
            source_file_name,
            target_path,
            source_format,
            target_format,
            font = font
        )

