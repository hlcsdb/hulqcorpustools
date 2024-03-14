
from flask import Request, current_app

from hulqcorpustools.utils.textcounter import TextCounter

def handle_request(request: Request) -> dict:

    if request.form.get("input") == "string":
        word_counter = current_app.text_counter
        word_counter.count_words(request.form.get("input-string"))

    elif request.form.get("input") == "files":
        word_counter = current_app.text_counter
        word_counter.count_file_words()
    
    response = {
        "word_count": word_counter.total
    }
    return response, 200