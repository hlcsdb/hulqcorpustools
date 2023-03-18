
from importlib import resources
import json

from . import graphemesdata

GRAPHEMES = json.load(resources.open_text(graphemesdata, "graphemes.json"))

