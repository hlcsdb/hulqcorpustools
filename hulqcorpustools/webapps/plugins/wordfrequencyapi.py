
from flask import Request

from hulqcorpustools.wordfrequency import WordCounter, FileWordCounter

def handle_request(request: Request) -> dict:

    if request.form.get("input") == "string":
        word_counter = WordCounter()
        word_counter.count_words(request.form.get("input-string"))

    elif request.form.get("input") == "files":
        word_counter = FileWordCounter(request.files.getlist("files"))
        word_counter.count_file_words()
    
    response = {
        "word_count": word_counter.total
    }
    return response, 200