
import itertools
import os
from pathlib import Path
from typing import Optional, Generator, Iterable
import time

from docxmanager import docxreader

class TotalCorpus():
    """the entire corpus file in one big text
    """
    def __init__(self,
        all_docx_files: list[docxreader.CorpusDocx]|Generator[docxreader.CorpusDocx, None, None],
        supplied_corpus_dir_path: Optional[Path] = None):
        """the CorpusDocx
        
        Arguments:
            all_docx_files -- a list of all the corpus docx files together
        """

        self.all_docx_files = all_docx_files
        self.corpus_dir = self._set_total_corpus_path(supplied_corpus_dir_path)
        self.corpus_path = self._generate_name()

    def _generate_name(
        self
        ):
        _timestamp = time.strftime('%Y-%m-%d-%H%M')
        self.corpus_filename = "%s%s%s" % ('Texts-corpus-', _timestamp, '.txt')
        self.corpus_path = self.corpus_dir.with_name(self.corpus_filename)
        return self.corpus_path

    def _set_total_corpus_path(
        self,
        _supplied_corpus_dir_path: Optional[Path] = None
    ):
        """return supplied corpus path, automatically generate from
        environment if not
        """
        if _supplied_corpus_dir_path:
            return _supplied_corpus_dir_path

        else:
            corpus_docx_env_path = Path(os.environ.get('CORPUS_DOCS_FOLDER'))
            default_corpus_dir = corpus_docx_env_path.parent / 'txt'
            self.corpus_dir = default_corpus_dir
            return default_corpus_dir

    def _generate_corpus_file_raw_text(
        self
        ):
        """_summary_

        Arguments:
            all_docx_files -- _description_
        """

        for _corpus_docx_file in self.all_docx_files:
            _file_name_line = '# ' + _corpus_docx_file.versionless_stem + '\n'
            _version_line = '# version: ' + _corpus_docx_file.version + '\n'
            _corpus_file_raw_text = itertools.chain(
                    [_file_name_line, _version_line], _corpus_docx_file._get_paragraph_text())

            yield _corpus_file_raw_text

    def _write_to_file(
        self,
        _corpus_text: itertools.chain[str, str, Generator]
        ):
        """_summary_

        Yields:
            _description_
        """
        with open(self.corpus_path, 'w') as _text_corpus_file:
            for _individual_corpus_text in _corpus_text:
                _file_comment = _individual_corpus_text.__next__()[:-1] # type: str
                print('writing ' + _file_comment + ' ...')
                _text_corpus_file.write(_file_comment)
                _text_corpus_file.writelines(_individual_corpus_text)

corpus_docs_folder = Path(os.environ.get('CORPUS_DOCS_FOLDER'))
corpus_docx_paths = corpus_docs_folder.glob('*.docx')
corpus_docx_files = (docxreader.CorpusDocx(_file) for _file in corpus_docx_paths)

if __name__ == "__main__":
    _corpus = TotalCorpus(corpus_docx_files)
    _corpus._write_to_file(_corpus._generate_corpus_file_raw_text())