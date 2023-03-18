
import itertools
import os
from pathlib import Path
from typing import Optional, Generator, Iterable
import time

from .docxtools.docxextractor import docx_text_extract

class TotalCorpus():
    """the entire corpus file in one big text file
    """
    def __init__(self,
        docx_file_list: list[Path],
        **kwargs
        ):
        """t
        
        Arguments:
            all_docx_files -- a list of all the corpus docx files together
        """
        self.docx_file_list = docx_file_list
        self.output_path = Path(kwargs.get('output_path'))
        if self.output_path:
            if self.output_path.is_dir():
                self.output_path = self.output_path / self._generate_corpus_filename()

        self.text_file_generators = self._get_corpus_docx_plaintext_generator()

    def _generate_corpus_filename(
        self
        ) -> Path:
        _timestamp = time.strftime('%Y-%m-%d-%H%M')
        self.corpus_filename = "%s%s%s" % ('Texts-corpus-', _timestamp, '.txt')
        return self.corpus_filename

    def _set_total_corpus_path(
        self,
        corpus_output_path: Optional[Path] = None
    ):
        """return supplied corpus path, automatically generate from
        environment if not
        """
        if corpus_output_path:
            return corpus_output_path

        else:
            corpus_docx_env_path = Path(os.environ.get('CORPUS_DOCS_FOLDER'))
            default_corpus_dir = corpus_docx_env_path.parent / 'txt'
            self.corpus_dir = default_corpus_dir
            return default_corpus_dir

    def _get_corpus_docx_plaintext_generator(self) -> list[Generator]:
        """get the generator that produces the raw text for each of the docx files

        Arguments:
            _docx_file_list -- _description_
        """

        return [docx_text_extract(docx_file) for docx_file in self.docx_file_list]
        

    # def _generate_corpus_file_raw_text(
    #     self
    #     ) -> Generator:
    #     """_summary_

    #     Arguments:
    #         all_docx_files -- _description_
    #     """

    #     for _corpus_docx_file in self.docx_file_list:
    #         _file_name_line = '# ' + _corpus_docx_file.versionless_stem + '\n'
    #         _version_line = '# version: ' + _corpus_docx_file.version + '\n'
    #         _corpus_file_raw_text = itertools.chain(
    #                 [_file_name_line, _version_line], _corpus_docx_file._get_paragraph_text())

    #         yield _corpus_file_raw_text

    def _write_to_file(
        self
        # _corpus_text: itertools.chain[str, str, Generator]
        ):
        """_summary_

        Yields:
            _description_
        """

        with open(self.output_path, 'w') as _text_corpus_file:
            for corpus_file_text_generator in self.text_file_generators:
                # # _file_comment = corpus_file_text_generator.__next__()[:-1] # type: str
                # print('writing ' + _file_comment + ' ...')
                # _text_corpus_file.write(_file_comment)
                _text_corpus_file.writelines(corpus_file_text_generator)