
from flask import Request

from hulqcorpustools.resources.constants import FileFormat
from hulqcorpustools.vocablookup.vocablookup import VocabLookup

class GroupedVocabLookups():

    apaunicode_lookup = VocabLookup(FileFormat.APAUNICODE)
    orthog_lookup = VocabLookup(FileFormat.ORTHOGRAPHY)

    # print(id(apaunicode_lookup), id(orthog_lookup))

    def __init__(self):
        ...

    def lookup_text(_text: str, text_format: str) -> dict:
        text_format = FileFormat.from_string(text_format)

        if text_format == FileFormat.APAUNICODE:
            _vl = GroupedVocabLookups.apaunicode_lookup
        elif text_format == FileFormat.ORTHOGRAPHY:
            _vl = GroupedVocabLookups.orthog_lookup

        _vl.collect_hulq_words_in_text(_text)
        _vl.vocab.sort_values('COUNT')
        vocab_found = _vl.vocab.to_dict(orient='index')
        known_words = _vl.found_known_words
        unknown_words = _vl.found_unknown_words
        results = {
            'vocab_found': vocab_found,
            'known_words': list(known_words),
            'unknown_words': list(unknown_words)
        }
        GroupedVocabLookups.orthog_lookup.reset_found_words()

        return results

    def lookup_file(_file: str, text_format: str) -> dict:
        text_format = FileFormat.from_string(text_format)

        # if text_format == FileFOrmat.
        ...

    def format_vocab_return():
        ...

def handle_submission(_request: Request):
    if _request.form.get('vocab-lookup-text'):
        vocab_lookup = handle_text(_request)
    elif _request.form.get('vocab-lookup-file'):
        ...
    return vocab_lookup


def handle_text(_request: Request):
    text_lookup = _request.form.get('input-text')
    text_format = _request.form.get('text-format')
    results_display_form = _request.form.get('results-display-form')
    lookup_results = GroupedVocabLookups.lookup_text(text_lookup, text_format)
    lookup_results.update({
        'text_lookup': text_lookup,
        'text_format': text_format,
        'results_display_form': results_display_form
    })
    return lookup_results
    ...

def handle_file(_request: Request):
    ...
