"""
loads grapheme file path 
"""
import os
from pathlib import Path
import json
default_json_path = Path(__file__).with_name('graphemes.json')

def open_graphemes_json(json_path):
    """returns a total dict made out of opening a json file with
    grapheme data in it
    """
    
    with open(json_path, 'r') as openjson:
        loaded_graphemes = json.load(openjson)

    return loaded_graphemes

loaded_graphemes = open_graphemes_json(default_json_path)