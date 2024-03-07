
from flask import Request, current_app

from hulqcorpustools.resources.constants import TextFormat
from hulqcorpustools.vocablookup.vocablookup import (
  VocabFinderFile,
  VocabFinder,
  Vocab
    )

def handle_submission(request: Request, **kwargs):
    vocab_db = current_app.vocab_db  # type: Vocab
    text_format = request.form.get("text-format")
    response = dict()

    if request.form.get("lookup-method") == "string":
        vocab_finder = VocabFinder(text_format, vocab_db)
        vocab_finder.find_vocab(request.form.get("input-string"))
        response.update({
            "input_string": request.form.get("input-string")
        })

    elif request.form.get("lookup-method") == "files":
        files_list = request.files.getlist("files")
        vocab_finder = VocabFinderFile(text_format, vocab_db, files_list)
        vocab_finder.find_vocab()
        response.update({
            "files": [file.filename for file in vocab_finder.file_list]
        })
        
    response.update(vocab_finder.results)
    response.update({"display_format": request.form.get("display-format")})
    return response, 200
