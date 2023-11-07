
from pathlib import Path

from flask import Blueprint, current_app, request, render_template, url_for, redirect, send_from_directory, Request
from werkzeug.utils import secure_filename

from .plugins.wordfrequencyapi import get_word_frequency_text, get_word_frequency_file


wordfrequency_bp = Blueprint('wordfrequency', __name__, url_prefix = '/', static_url_path='', static_folder='')

ALLOWED_EXTENSIONS = {'.txt', '.docx', '.doc'}

@wordfrequency_bp.route("/word-frequency", methods=['GET', 'POST'])
def word_frequency_page():
    current_version = current_app.config['CURRENT_VERSION']
    if request.method == 'POST':
        response_dict = handle_word_count_request(request)
        return render_template(
            'word-frequency.html', 
            word_counts=word_counts)
    return render_template('word-frequency.html', current_version=current_version)

def handle_word_count_request(_request: Request):
    if _request.form.get('word-frequency-text'):
        word_count = wf_api.string_word_count(_request.form.get('input-text'))

    elif _request.form.get('word-frequency-file'):
        count_from_file = handle_file_word_count_request(_request)
        return count_from_file 

def handle_file_word_count_request(_request: Request):

def handle_file_word_count_request(_request: Request):
    uploaded_files_list = request.files.getlist('word-count-files')
    
    if uploaded_files_list[0].filename == '':
        return redirect(_request.url)

    for _file in uploaded_files_list:
        _file.filename = secure_filename(_file.filename)

    uploaded_files_list = list(filter(allowed_file, uploaded_files_list))

    UPLOADS_FOLDER = current_app.config['UPLOADS_FOLDER']
    upload_dir = Path(UPLOADS_FOLDER)

    uploaded_file_paths = []

    for _file in uploaded_files_list:
        upload_path = Path(upload_dir.joinpath(_file.filename))
        _file.save(upload_path)
        uploaded_file_paths.append(upload_path)

    word_count = wf_api.file_word_count(uploaded_file_paths)

    return word_count


def allowed_file(file):
    filename = Path(file.filename)
    if filename.suffix in ALLOWED_EXTENSIONS:
        return True
    else:
        return False