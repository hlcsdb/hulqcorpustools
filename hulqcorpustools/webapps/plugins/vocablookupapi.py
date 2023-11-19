
from pathlib import Path

from flask import Request

from .common import save_secured_allowed_files_to_path

from hulqcorpustools.resources.constants import FileFormat
from hulqcorpustools.vocablookup.vocablookup import VocabFinderFilehandler, VocabFinder
from hulqcorpustools.utils.files import FileHandler

def handle_submission(_request: Request, **kwargs):
    if _request.form.get('vocab-lookup-text'):
        vocab_lookup = handle_text(_request)
    elif _request.form.get('vocab-lookup-files'):
        vocab_lookup = handle_files(_request, kwargs['upload_dir'])

    else:
        return ''
    
    return vocab_lookup


def handle_text(_request: Request) -> dict:
    text_lookup = _request.form.get('input-text')
    text_format = _request.form.get('text-format')
    results_display = _request.form.get('results-display')

    finder = VocabFinder(text_format)
    lookup_results = finder.lookup_string(text_lookup)
    lookup_results.update({
        'text_lookup': text_lookup,
        'text_format': text_format,
        'results_display': results_display
    })
    return lookup_results
    ...

def handle_files(
        _request: Request,
        upload_dir: str) -> dict:
    
    if len(_request.files) < 1:
        return

    files_lookup_list = _request.files
    _filenames = [_file.filename for _file in _request.files.getlist('vocab-lookup-files')]
    files_saved = save_secured_allowed_files_to_path(
        files_lookup_list,
        'vocab-lookup-files',
        upload_dir)
    files_saved_paths = [_file.filename for _file in files_saved]

    text_format = _request.form.get('text-format')
    results_display = _request.form.get('results-display')

    file_finder = VocabFinderFilehandler(
        files_saved_paths,
        text_format
        )
    
    lookup_results = file_finder.all_results
    lookup_results.update({
        'file_names': _filenames,
        'text_format': _request.form.get('text-format'),
        'results_display': results_display
        })
    
    return lookup_results