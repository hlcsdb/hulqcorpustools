
# from pydantic.dataclasses import dataclass, Field
from dataclasses import dataclass, field
from typing import Optional

@dataclass
class Author():

    name: str
    author_code: str
    hulq_name: Optional[str] = None
    bio: Optional[str] = None

    @property
    def author_text(self):
        if self.hulq_name is not None:
            return f"A\t{self.name} - {self.hulq_name}"

        else:
            return f"A\t{self.name}"


@dataclass
class CorpusMetadata():

    eng_title: str
    story_code: str
    authors: list = field(default_factory=list)
    hulq_title: Optional[str] = None


@dataclass
class TextLine():

    line_type: str
    text: str

    @classmethod
    def line_must_be_hulq_or_english(cls, line_type: str) -> str:
        if line_type not in ["hulq", "eng"]:
            raise ValueError("line type must be either 'hulq' or 'eng'")
        return line_type

    def __repr__(self):
        return self.text


@dataclass
class CorpusLine():

    line_number: int
    story_code: str
    hulq: Optional[TextLine] = None
    eng: Optional[TextLine] = None
    notes: list = field(default_factory=list)

    @property
    def citation(self):
        return f"{self.story_code}.{self.line_number}"

    @property
    def hulq_text(self):
        return f"LH\t{self.hulq}"

    @property
    def eng_text(self):
        return f"LE\t{self.eng}"

    @property
    def notes_text(self):
        notes_annotated = '\n'.join([f"N\t{note}" for note in self.notes])
        return notes_annotated

    def text_render(self, verbose=False):
        text_parts = [
            self.hulq_text,
            self.eng_text,
            self.notes_text,
            self.citation
        ]

        return "\n".join(text_parts)


@dataclass
class CorpusText():

    metadata: CorpusMetadata
    text: list = field(default_factory=list[CorpusLine])

