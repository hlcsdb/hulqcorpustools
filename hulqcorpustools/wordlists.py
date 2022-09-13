"""Loads the paths to any wordlists to be opened as needed"""

from enum import Enum
from pathlib import Path

import pandas as pd

from resources.constants import FileFormat


_wordlists_dir_path = Path(__file__).resolve().parent / \
        'resources' / 'wordlists'

def _get_wordlist_path(
    wordlists_dir_path: Path,
    file_format: FileFormat | str,
    **kwargs) -> Path:
    """get the path for the new wordlist for a given file format"""

    # if passed FileFormat -- turn it to string
    if type(file_format) == FileFormat:
        file_format = file_format.to_string()
    else:
        # check for spelling -- raises error if spelt wrong
        FileFormat.from_string(file_format)

    # construct filename
    wordlist_filename = \
        'hulq-wordlist-' + file_format + '.txt'

    if kwargs.get('new') is True:
        wordlists_dir_path = \
        wordlists_dir_path / 'new-wordlists'
        wordlist_filename = 'new-' + wordlist_filename

    wordlist_path = Path(wordlists_dir_path / wordlist_filename)
    return wordlist_path

class Wordlists(Enum):
    """Lists of paths to the wordlists accessible by CONSTANT.value
    """
    HULQ_WORDLISTS: dict = \
        {file_format.to_string(): _get_wordlist_path(_wordlists_dir_path,file_format) for file_format in
        FileFormat.file_formats()}

    NEW_WORDLISTS: dict = \
        {file_format.to_string(): _get_wordlist_path(_wordlists_dir_path, file_format, new=True) for file_format in
        FileFormat.file_formats()}

    ENGLISH_WORDLIST: dict = \
        {'english': _wordlists_dir_path / 'other-wordlists' / 'english-wordlist.txt'}

    ALL_WORDLISTS = \
        {**HULQ_WORDLISTS, **NEW_WORDLISTS, **ENGLISH_WORDLIST}

### these might be orphans now
    def get_xlsx_paths(*args) -> dict:
        """gets a dict of any wordlists in xlsx format

        Returns:
            a dict of the path of form {'xlsx_wordlists' : []}
        """
        xlsx_paths = Path(__file__).parent.glob('*.xlsx')
        xlsx_wordlists = {'xlsx_wordlists': [i for i in xlsx_paths]}
        return xlsx_wordlists

    def open_xlsx_dict(xlsx_path: Path, *args) -> pd.DataFrame:
        """
        opens a dict from an xlsx file into a pandas df
        Arguments:
            xlsx_path -- path to the xlsx file

        Returns:
            xlsx_df -- a pandas df
        """
        xlsx_df = pd.read_excel(xlsx_path)

        return xlsx_df

    def write_wordlist_to_txt(output_filename: str, wordlist_df: pd.DataFrame):
        """writes the line of the pandas dataframe in the hukari peter dict
        to a txt file

        Arguments:
            wordlist_df: the dataframe with a wordlist in it
        """
        wordlist = wordlist_df.get('LEXEME - curly ’unuhw')
        output_path = Path(__file__).parent / output_filename
        with open(output_path, 'w+') as open_file:
            for i in wordlist:
                open_file.write(''.join([i.strip(), '\n']))

    # hukari_peter_xlsx_path = get_xlsx_paths().get('xlsx_wordlists')[0]
    # hukari_peter_xlsx_df = open_xlsx_dict(hukari_peter_xlsx_path)



if __name__ == '__main__':
    ...