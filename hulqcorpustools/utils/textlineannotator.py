
import re

from .languagesusser import determine_language_from_text as dlt
from ..resources.constants import FileFormat

class TextlineAnnotation():
    """Some of the plaintext annotations to put at the beginning of a line,
    placed in a class so it doesn't need to be substantiated for each par.
    """

    existing_bibliographic_anno = \
        ["Title\s",
        "T\s",
        "Author[\s\:]?",
        "A\t",
        "Notes",
        "Note"
        "N\s",
        "N\t",
        "C\t",
        "U\t"]

    existing_line_anno = \
        ["LH\s",
        "LE\s"]

    anno_bib_regex = re.compile('(' + '|'.join(existing_bibliographic_anno) + ')')
    existing_line_anno = re.compile('(' + '|'.join(existing_bibliographic_anno + existing_line_anno) + ')')

    @classmethod
    def annotate_line(cls, textline: str, **kwargs):
        """Annotate line of text with appropriate corpus tag.

        Arguments:
            textline -- A line of text.

        Returns:
            The line of text with an initial tag followed by a tab (\t).
        """

        # first: see if the line has already been annotated, that is, if the
        # initial characters are an annotation tag
        existing_line_anno = re.finditer(cls.anno_bib_regex, textline)
        found_bib = False
        new_text = textline

        for i in existing_line_anno:
            found_bib = True
            replace_anno = i.group()[0] + '\t'
            new_text = re.sub(i.re, replace_anno, new_text)
                
            
        # otherwise: try to annotate the line
        if found_bib is False:
            determined_language = dlt(textline)
            
            if determined_language in [FileFormat.ORTHOGRAPHY, FileFormat.APA_UNICODE]:
                new_text = f'LH\t{textline}'

            elif determined_language == FileFormat.ENGLISH:
                new_text = f'LE\t{textline}'

            else:
                if kwargs.get('verbose') is not None:
                    print(f'cannot determine:\n{textline}')
                new_text = f'U\t{textline}'
        return new_text