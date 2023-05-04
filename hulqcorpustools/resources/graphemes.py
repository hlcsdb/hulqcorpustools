
from importlib import resources
import json

from . import graphemesdata

loaded_graphemes = json.load(resources.open_text(graphemesdata, "graphemes.json"))

