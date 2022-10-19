
import os
from importlib import resources
from pathlib import Path

from docx import Document

from hulqcorpusresources import corpusparts

if __name__ == "__main__":
    test_corpus_file_list = list(Path(os.environ.get('CORPUS_TEST_DATA_FOLDER')).glob('*.docx'))
    # for _file in test_corpus_file_list:
    #     if '~$' in _file.stem:
    #         test_corpus_file_list.remove(_file)
    # test_corpus_file = docx.Document(test_corpus_file_list[0])
    # for i in test_corpus_file.paragraphs[0:1000]:
        
    #     _DocxCorpusTextLine(i)