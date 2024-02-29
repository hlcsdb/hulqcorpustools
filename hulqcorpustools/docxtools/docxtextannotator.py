
"""Put a direct text annotation at the beginning of all lines in a docx file.
"""

from pathlib import Path
import re

import docx

from ..utils.languagesusser import determine_language_from_text as dlt
from ..utils.textlineannotator import TextlineAnnotation
from ..resources.constants import TextFormat

class DocxParagraphTextAnnotations(TextlineAnnotation):
    """Some of the plaintext annotations to put at the beginning of a line,
    placed in a class so it doesn't need to be substantiated for each par.
    """

    @classmethod
    def _annotate_docx_par(cls, paragraph_text):
        """Roughly annotate the type of the line according to the information in the line.

        Arguments:
            paragraph -- a line of text from a docx Paragaph
        """
        new_text = TextlineAnnotation.annotate_line(paragraph_text)
        return new_text

    @classmethod
    def _annotate_all_docx_pars(cls, corpus_docx_file: docx.document.Document) -> docx.document.Document:
        """Annotate all the lines in a corpus docx file with some qualifications
        stipulated in annotate_docx_line.

        Arguments:
            corpus_docx_file -- the path to a docx file to put in the corpus
        """

        for paragraph in corpus_docx_file.paragraphs:
            # split lines and discard extra space
            
            paragraph_text = [line for line in paragraph.text.splitlines() if len(line) > 0]
            
            # do nothing if nothing is in the line
            if len(paragraph_text) == 0:
                continue

            # annotate each line of text, more than one if there is a linebreak
            elif len(paragraph_text) >= 1:
                new_text = [cls._annotate_docx_par(paragraph_line) for paragraph_line in paragraph_text]
                paragraph.text = '\n'.join(new_text)
                continue
                
        return corpus_docx_file

    @classmethod
    def annotate_docx_file(cls, docx_filepath: Path, **kwargs):
        """ask a docx file to be annotated and save a new version of it

        Arguments:
            docx_filepath -- path to a docx file
        Kwargs:
            output_path: desired output Path
        """


        output_path = kwargs.get('output_path') # type: Path
        verbose = kwargs.get('verbose')
        new_docx_name = None # initialize docx name
        docx_document = docx.Document(docx_filepath)

        # construct output filepath
        if output_path is not None: # use desired path if provided
            output_path = Path(output_path)
        
        else: # make default folder
            output_dir = docx_filepath.parent / 'annotated'
            if output_dir.exists() is False:
                output_dir.mkdir()

        # if no new name is provided: come up with default "annotated" name
        if new_docx_name is None:
            new_docx_name = Path(docx_filepath.stem + ' annotated').with_suffix(docx_filepath.suffix)
            output_path = output_path / new_docx_name # make new name
            
        # resolve in case of relative path
        output_path = output_path.resolve()

        if verbose is not None:
            print(f'#####\ndocx_filename = {docx_filepath}\nnew_docx_name = {new_docx_name}\noutput_path = {output_path}\n')

        annotated_docx = cls._annotate_all_docx_pars(docx_document)
        annotated_docx.save(output_path)