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

    def open_xlsx_dict(xlsx_path: Path, *args):
        """
        # TODO: save 
        
        opens a dict from an xlsx file into a pandas df

        Arguments:
            xlsx_path -- _description_

        Returns:
            _description_
        """
        xlsx_df = pd.read_excel(xlsx_path)

        return xlsx_df

    wordlist_paths = get_wordlist_paths()
    xlsx_paths = get_xlsx_paths()

    hukari_peter_df = open_xlsx_dict(xlsx_paths.get('xlsx_wordlists')[0])


    

if __name__ == '__main__':
    hukari_peter_xlsx = HulqWordlists.hukari_peter_df
    cool = hukari_peter_xlsx.get(['LEXEME - curly ’unuhw'])
    print(cool)