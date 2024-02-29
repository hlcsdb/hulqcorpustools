"""Approximate spellings in Hul’q’umi’num’ for easier lookup.

Inspired by roedoejet/g2p, but implemented here for simplicity of specific use.

    #TODO: these should be in a utils 
"""

import csv
from pathlib import Path
from importlib.resources import files
import re

class Mapping():
    """Define a mapping between the 

    Returns:
        _description_
    """
    
    def __init__(self, mapping_path: Path):
        """Init with Path to csv containing simple mapping pairs
        

        Arguments:
            mapping_path -- Path of pairs a,b where a should be
            respresented as b
        """
        self.mapping_dict = {
            mapping_pair[0]: mapping_pair[1]
            for mapping_pair in csv.reader(open(mapping_path))
        }
        self.mapping_re = self._generate_mapping_re(self.mapping_dict)

    def _generate_mapping_re(self, mapping_dict: dict):
        """generate a list of regex expressions that represent all needed mappings

        Arguments:
            mapping_list -- _description_
        """
        mapping_pair_re_string = '|'.join(
            map(re.escape, (mapping_initial for mapping_initial
            in mapping_dict.keys())
            )
        )
        mapping_pair_re = re.compile(mapping_pair_re_string)

        return mapping_pair_re

class Transducer():
    """renders word in one form to another form according to a Mapping
    """
    def __init__(self, mapping: Mapping):
        self.mapping = mapping
        self.mapping_dict = mapping.mapping_dict
        self.mapping_re = mapping.mapping_re

    def transduce(self, word: str):
        """transduce word from one form to another
        """
        transduced_word = self.mapping_re.sub(
            lambda match: self.mapping_dict[match.group(0)], word)
        return transduced_word

approximator = Transducer(Mapping(files(__package__) / "approximate.csv"))
weak_approximator = Transducer(Mapping(files(__package__) / "weak_approximate.csv"))
