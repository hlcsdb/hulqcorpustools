
from dataclasses import dataclass, field
from pathlib import Path
from pprint import pprint
import xml.etree.ElementTree as ET

from hulqcorpustools.resources import textannotations as textanno

@dataclass
class CorpusLine():
    """A line of text from the corpus.
    """
    line_number = int
    line_hulq: str = None
    id: str = ''
    line_english: list[str] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)
    plaintext_line_number = int = 0

    def add_english_line(self, eng: str):
        if not self.line_english:
            self.line_english = []
        
        self.line_english.append(eng)

    
    def _set_id(self, outer_pfx, id_pfx=None):
        """Set the xml:id prefix according to provided prefix, generating one
        if needed.

        Keyword Arguments:
            outer_pfx -- The outer prefix from the text prefix.

        """
        
        self.id = f"{outer_pfx}.{self.plaintext_line_number}"

    def _to_element(self):
        """Converts current line to ElementTree.
        """
        line_element = ET.Element('line',
        attrib={"lineno": str(self.line_number),
        "xml:id": f"{self.id}"})
        # TODO:
        # decide whether I want every line to need Hul’q’umi’num’
        if self.line_hulq:
            hulq_element = ET.SubElement(line_element, "hulq")
            hulq_element.text = self.line_hulq
        if self.line_english:
            for i in self.line_english:
                eng_element = ET.SubElement(line_element, "english")
                eng_element.text = i
        if self.notes:
            notes_element = ET.SubElement(line_element, "notes")
            for note in self.notes:
                note_element = ET.SubElement(notes_element, "note")
                note_element.text = note

        return line_element


@dataclass
class CorpusBody():
    """The body text of the corpus.
    """
    notes: list[str] = field(default_factory=list)
    id_pfx: str = ''
    body_lines: list[CorpusLine] = field(default_factory=list)

    def _to_element(self):
        body_element = ET.Element('text_body')

        for line in self.body_lines:
            body_line_element = line._to_element()
            
            body_element.append(body_line_element)

        if self.notes:
            notes_element = ET.SubElement(body_element, 'text_notes')
            for i in self.notes:
                note_element = ET.SubElement(notes_element, 'note')
                note_element.text = i

        # print(self.body_lines)
        return body_element


@dataclass
class CorpusText():
    """A text (usually a story) in line-by-line form.
    """
    text_title: str
    id_pfx: str = ''
    text_body: CorpusBody = CorpusBody()
    authors: set[str] = field(default_factory=set)
    notes: list[str] = field(default_factory=list)

    def _set_id_pfx(self, outer_pfx, **kwargs):
        """Set the xml:id prefix according to provided prefix, generating one
        if needed.

        Keyword Arguments:
            outer_pfx -- The outer prefix from the collection prefix.

        Returns:
            _description_
        """
        if kwargs.get('id_pfx') is None:
            title_initials = [word[0] for word in self.text_title.translate(str.maketrans({"’" : None, "-" : None})).split()]
            self.id_pfx = ''.join(title_initials)

        if kwargs.get('authors'):
            author_initial_pairs = [''.join([name[0] for name in kwargs.get('authors')])]
            author_initials = '+'.join([initial for initial in author_initial_pairs])
            self.id_pfx = f'{author_initials}.{self.id_pfx}'
                
        self.id_pfx = f"{outer_pfx}.{self.id_pfx}"

    def _to_element(self):
        """Converts self to ElementTree.
        """
        text_element = ET.Element('text')
        text_title_element = ET.SubElement(text_element, 'text_title',
        attrib={"xml:id" : self.id_pfx})
        text_title_element.text = self.text_title

        text_authors_element = ET.SubElement(text_element, "text_authors")
        for i in self.authors:
            text_author_element = ET.SubElement(text_authors_element, 'text_author')
            text_author_element.text = i

        if self.notes:
            notes_element = ET.SubElement(text_element, 'text_notes')
            for i in self.notes:
                note_element = ET.SubElement(notes_element, 'note')
                note_element.text = i

        text_element.append(self.text_body._to_element())

        return text_element


@dataclass
class CorpusCollection():
    """A collection of stories.
    """
    collection_title: str = ''
    id_pfx: str = ''
    collection_texts: list[CorpusText] = field(default_factory=list)
    authors: set[str] = field(default_factory=set)
    notes: list = field(default_factory=list)

    def _set_id_pfx(self, id_pfx=None):
        """Set xml:id prefix, generating one if none is provided.

        Arguments:
            id_pfx: A desired id_pfx noted in the text.
        """
        if id_pfx is None:
            # If no id_pfx is provided, generate based on title initials
            id_pfx = ''.join([word[0] for word in self.collection_title.split()])
        
        self.id_pfx = id_pfx

    def _to_element(self):
        collection_element = ET.Element('collection', attrib={
            "xml:id": self.id_pfx})
        collection_title_element = ET.SubElement(collection_element, 'collection_title')
        collection_title_element.text = self.collection_title

        collection_authors_element = ET.SubElement(collection_element, 'collection_authors')
        for i in self.authors:
            collection_author_element = ET.SubElement(collection_authors_element, 'author')
            collection_author_element.text = i

        if self.notes:
            collection_notes_element = ET.SubElement(collection_element, 'collection_notes')
            for i in self.notes:
                collection_note_element = ET.SubElement(collection_notes_element, 'collection_note')
                collection_notes_element.text = i

        collection_texts_element = ET.SubElement(collection_element, 'texts')
        for text in self.collection_texts:
            collection_texts_element.append(text._to_element())

        return collection_element


@dataclass
class CorpusFile():
    """One corpus to be returned as an ElementTree Element.
    """
    corpus_collections: list[CorpusCollection] = field(default_factory=list)
    has_error: bool = False
    lines_with_error: list[(int, str)] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)

    def _to_element(self):
        """_summary_
        """

        corpus_element = ET.Element('corpus')

        if self.has_error:
            error_lines_element = ET.SubElement(corpus_element, 'error_lines')
            for i in self.lines_with_error:
                error_line_element = ET.SubElement(error_lines_element, 'error', {
                    'xml:id' : str(i[0]),
                    'errortexttitle' : str(i[2]),
                    'errortextlineno' : str(i[3])})
                error_line_element.text = i[1]

        for collection in self.corpus_collections:
            corpus_element.append(collection._to_element())
            
        if self.notes:
            notes_element = ET.SubElement(corpus_element, 'corpus_notes')
            for i in self.notes:
                note_element = ET.SubElement(notes_element, 'note')
                note_element.text = i

        return corpus_element

class IdPrefix():
    """the current ID prefix
    """
    ...

def make_xml_corpus(txtfile_path: Path, **kwargs):
    """Make a single basic version of an XML corpus.

    Arguments:
        txtfile_paths -- a list of Paths to be compiled into one XML corpus
    Kwargs:
        output_path: the desired output path
    """

    output_path = kwargs.get('output_path')

    if not output_path:
        output_path = txtfile_path.with_suffix('.xml')

    if output_path.is_dir():
        output_path = Path(output_path / txtfile_path.name).with_suffix(".xml")

    corpus_xml = _start_parse_plain_text(txtfile_path)
    corpus_xml.write(output_path, encoding="utf-8")

def _start_parse_plain_text(txtfile_path: Path):
    """Start to parse a plaintext file.

    Arguments:
        txtfile_path -- Path to a corpus-annotated .txt file.
    """

    with open(txtfile_path, 'r') as corpus_txt:
        corpus_element = _parse_plain_text(corpus_txt.readlines())
        corpus_tree = ET.ElementTree(corpus_element)
        ET.indent(corpus_tree)

        return corpus_tree

def _parse_plain_text(txtfile:list[str], **kwargs):
    """Parse a plaintext corpus file to XML.

    Arguments:
        txtfile_path -- Path to a corpus-annotated .txt file.
    """
    verbose = kwargs.get('verbose')

    current_corpus_file = CorpusFile()
    current_pointer = current_corpus_file
    current_corpus_line = None
    current_text_line_number = 0
    current_corpus_body = None
    current_corpus_text = None
    current_corpus_collection = None
    current_plaintext_line_number = 0
    current_prefix = str()

    def _throw_error(line, **kwargs):
        if kwargs.get('verbose') is True:
                print("*** Error! *** The following line is not annotated correctly:")
                print(line)
                print("Please go back and annotate this line. The corpus is now marked as having an error at this line number.")
        current_corpus_file.has_error = True
        if current_corpus_text:
            error_text_title = current_corpus_text.text_title
        else:
            error_text_title = "preamble"
        current_corpus_file.lines_with_error.append((current_plaintext_line_number, line, error_text_title, current_text_line_number))

    for line in txtfile:
        current_plaintext_line_number += 1
        line = line.strip()
        if len(line) <= 3:
            continue
        
        elif line[0:2] == "C\t":
            current_corpus_collection = CorpusCollection(line[2:])
            current_corpus_file.corpus_collections.append(current_corpus_collection)
            current_pointer = current_corpus_collection

        elif line[0:2] == "T\t":
            # indicating start of a new text

            if current_corpus_text:
                # if it's not the first text, then the last one just finished
                current_corpus_body.body_lines.append(current_corpus_line)
                current_corpus_collection.collection_texts.append(current_corpus_text)
                current_corpus_line = None
            
            current_text_line_number = 0
            current_corpus_text = CorpusText(line[2:])

            current_prefix = current_corpus_text._set_id_pfx(current_corpus_collection.id_pfx)
            current_corpus_body = CorpusBody()
            current_corpus_text.text_body = current_corpus_body
            current_pointer = current_corpus_text

        elif line[0:4] == "PFX\t":
            current_prefix = line[4:]
            current_pointer.id_pfx = line[4:]

        elif line[0:2] == "A\t":

            if current_pointer.__class__ in (CorpusCollection, CorpusText):
                current_pointer.authors.add(line[2:])
        

        elif line[0:2] in ("N\t", "B\t"):
            try:
                current_pointer.notes.append(line[2:])
            except AttributeError:
                _throw_error(line)


        elif line[0:2] == "B\t":
            current_pointer.notes.append(line[3:])

        elif line[0] == "L" and "\t" in line[2:3]:
            
            # initialize a current line
            if not current_corpus_line:
                current_text_line_number = 0
                # current_corpus_line = CorpusLine()
                # current_corpus_line.line_number = current_text_line_number
                # current_corpus_line.plaintext_line_number = current_plaintext_line_number
            


            if line[0:2] == "LH":

                if current_corpus_line:
                    # if the current line already has a line of Hul’q’umi’num’,
                    # it is always time for a new line
                    current_corpus_body.body_lines.append(current_corpus_line)

                current_text_line_number += 1
                current_corpus_line = CorpusLine()
                current_corpus_line.line_hulq = line[3:]
                current_corpus_line.line_number = current_text_line_number
                current_corpus_line.plaintext_line_number = current_plaintext_line_number


            elif line[0:2] == "LE":

                if not current_corpus_line:
                    current_text_line_number += 1
                    current_corpus_line = CorpusLine()
                    current_corpus_line.line_number = current_text_line_number
                    current_corpus_line.plaintext_line_number = current_plaintext_line_number
                    

                current_corpus_line.add_english_line(line[3:])

            current_corpus_line._set_id(current_corpus_text.id_pfx)
            
            current_pointer = current_corpus_line
            


        else:
            _throw_error(line)

            continue

    return current_corpus_file._to_element()