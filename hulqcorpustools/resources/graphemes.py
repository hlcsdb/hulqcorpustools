
from importlib.resources import files, as_file
import json

grapheme_file = files(__package__) / "graphemes.json"
loaded_graphemes = json.load(open(grapheme_file))