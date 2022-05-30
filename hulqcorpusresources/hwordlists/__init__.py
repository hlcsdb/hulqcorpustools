import os
import pandas as pd
from pathlib import Path
import typing
# from constants import FileFormat

class HulqWordlists():
    '''
    class that allows for easy retrieval of some of the wordlists
    '''
    def get_wordlist_paths(*args) -> dict:
        """gets a dict of wordlist paths for a given category

        Args:
            (): returns dict of the regular wordlist paths
            'new': returns dict of paths to the wordlists in 'new-wordlists'
                which are those to be updated
            'other': returns dict of the paths to wordlists in 'other-wordlists'
                which are mostly just long English wordlists
            
            'all': returns a dict of paths to all wordlists
        Returns:
            dict of wordlists
        """
        wordlist_paths = list()

        if 'new' in args or 'all' in args:
            new_wordlists_path = Path(__file__).parent / 'new-wordlists'
            wordlist_paths.append(new_wordlists_path)

        if 'other' in args or 'all' in args:
            other_wordlists_path = Path(__file__).parent / 'other-wordlists'
            wordlist_paths.append(other_wordlists_path)
        
        if not args or 'all' in args:
            normal_wordlists_path = Path(__file__).parent
            wordlist_paths.append(normal_wordlists_path)

        return wordlist_paths

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

    hukari_peter_xlsx_path = get_xlsx_paths().get('xlsx_wordlists')[0]
    hukari_peter_xlsx_df = open_xlsx_dict(hukari_peter_xlsx_path)



if __name__ == '__main__':
    HulqWordlists.write_wordlist_to_txt('hukari_peter_wordlist.txt', HulqWordlists.hukari_peter_xlsx_df)