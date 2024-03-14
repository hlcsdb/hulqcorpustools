
from flask import Request, current_app

from hulqcorpustools.vocablookup.vocablookup import (
  VocabFinder,
  Vocab
    )

def handle_submission(request: Request, **kwargs):
    vocab_db = current_app.vocab_db  # type: Vocab
    text_counter = current_app.text_counter
    text_format = request.form.get("text-format")
    response = dict()
    vocab_finder = VocabFinder(
        text_format,
        vocab_db,
        text_counter
        )

    if request.form.get("lookup-method") == "string":
        vocab_finder.find_vocab(request.form.get("input-string"))
        response.update({
            "input_string": request.form.get("input-string")
        })

    elif request.form.get("lookup-method") == "files":
        file_list = request.files.getlist("files")
        vocab_finder.find_vocab_file(file_list)
        response.update({
            "files": [file.filename for file in file_list]
        })
        
    response.update(vocab_finder.results)
    response.update({"display_format": request.form.get("display-format")})
    return response, 200
