
from pathlib import Path

from flask import Blueprint, current_app, request, render_template, url_for, redirect, send_from_directory
from werkzeug.utils import secure_filename

from .plugins.wordfrequencyapi import get_word_frequency_text, get_word_frequency_file

wordfrequency_bp = Blueprint('wordfrequency', __name__, url_prefix = '/', static_url_path='', static_folder='')

ALLOWED_EXTENSIONS = {'.txt', '.docx'}

@wordfrequency_bp.route("/word-frequency", methods=['GET', 'POST'])
def word_frequency_page():
    if request.method == 'POST':
        word_counts = handle_word_count_request(request)
        return render_template(
            'word-frequency.html', 
            word_counts=word_counts)
    return render_template('word-frequency.html')

def handle_word_count_request(_request: request):
    if _request.form.get('word-frequency-text'):
        return get_word_frequency_text(_request.form.get('input-text'))

    elif _request.form.get('word-frequency-file'):
        count_from_file = handle_file_word_count_request(_request)
        return count_from_file 

def handle_file_word_count_request(_request):

    if 'word-count-file' not in _request.files:
        return redirect(_request.url)
    
    file = _request.files['word-count-file']
    print(file)
    if allowed_file(file) is False:
        return redirect(_request.url)
    
    filename = secure_filename(file.filename)
    UPLOAD_FOLDER = current_app.config['UPLOAD_FOLDER']
    upload_dir = Path(UPLOAD_FOLDER)
    upload_path = upload_dir.joinpath(filename)
    file.save(upload_path)

    counted_file = get_word_frequency_file(upload_path)

    return counted_file


def allowed_file(file):
    filename = Path(file.filename)
    if filename.suffix in ALLOWED_EXTENSIONS:
        return True
    else:
        return False