
from pathlib import Path

from flask import Request

from .common import save_safe_files

from hulqcorpustools.resources.constants import FileFormat
from hulqcorpustools.vocablookup.vocablookup import VocabFinderFile, VocabFinder
from hulqcorpustools.utils.files import FileHandler

def handle_submission(_request: Request, **kwargs):
    _submission = {}
    if _request.form.get('text-lookup'):
        _submission = SubmissionHandler(_request)

        # lazy evaluation in case other things should be added later
        _submission.lookup_vocab()

    elif _request.form.get('files-lookup'):
        _submission = FileSubmissionHandler(
            _request,
            upload_dir = Path(kwargs.get('upload_dir')))
        
        _submission.lookup_vocab()

    return _submission.response

class SubmissionHandler():
    """Class to handle form submissions from vocablookup site.

    Once submission is dealt with, get the response results from results
    property.
    """
    def __init__(
            self,
            _request: Request,
            **kwargs
            ):
        """Receive request from user, delegating to text or file submission.

        Args:
            _request (Request): the Flask request with all of the information
            from the form submission.
        """

        """
        upload_dir: path to where files are uploaded in case of file submission

        Returns:
        dict with response details and vocab lookup results:
        {vocab_found:
            {ID1: {dictionary results... },
            {ID2: {dictionary results, ...},
            ...
        }
        """

        self.request = _request
        self.text_format = _request.form.get('text-format')
        self.results_display_format = _request.form.get('results-display-format')
        self._response = {}

    def lookup_vocab(self):
        self.vocab_finder = VocabFinder(self.text_format)
        _text = self.request.form.get('input-text')
        self._response.update({
            'text_lookup': _text
        })
        self.vocab_finder.find_vocab_in_text(_text)

    @property
    def response(self) -> dict:
        self._response.update(self.vocab_finder.vocab)
        self._response.update({
            'text_format': self.text_format,
            'results_display_format': self.results_display_format
        })
        return self._response

class FileSubmissionHandler(SubmissionHandler):

    def __init__(
            self,
            _request: Request,
            upload_dir: str | Path
            ):
        """Handle a request to look up vocab in submitted files.

        Args:
            files
            upload_dir -- the directory where the files to search are saved

        Returns:
            dict with response details and vocab lookup results

        Args:
            files (Request.files): a list of files in a Flask/Werkzeug Request
            text_format (str | FileFormat): the text format of the files
            upload_dir (str | Path): the directory to save the files 
        """

        super().__init__(_request)

        # files in stream from submission form must be saved to filesystem
        # to allow program to have access so they may be read
        self.files_saved = save_safe_files(
            _request.files,
            'files-lookup',
            upload_dir
        )

        # just for file name with no full path
        self.saved_file_paths = [_file.filename for _file in self.files_saved]
        file_handler = FileHandler(self.saved_file_paths)
        self._response.update({
            'file_list': [_file.name for _file in self.saved_file_paths]
        })
        
        self.vocab_finder = VocabFinderFile(
            self.text_format,
            self.saved_file_paths
        )

    def lookup_vocab(self):
        self.vocab_finder.find_vocab_in_files()

def handle_text(_request: Request) -> dict:
    """Handle a text request and return vocab lookup results

    Arguments:
        _request: Flask Request with vocab lookup submission details

    Returns:
        dict with response details and vocab lookup results (see handle_submission)
    """
    text_lookup = _request.form.get('input-text')
    text_format = _request.form.get('text-format')
    results_display_format = _request.form.get('results-display-format')

    finder = VocabFinder(text_format)
    lookup_results = finder.find_vocab_in_text(text_lookup)
    lookup_results.update({
        'text_lookup': text_lookup,
        'text_format': text_format,
        'results_display_format': results_display_format
    })
    return lookup_results
    ...