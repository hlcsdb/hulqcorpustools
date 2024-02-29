
from pathlib import Path

from flask import Blueprint, current_app, request, render_template, url_for, redirect
from flask.wrappers import Request, Response
from werkzeug.utils import secure_filename

from ..plugins import wordfrequencyapi as wf_api
from ..plugins.common import allowed_file, save_safe_files

wordfrequency_bp = Blueprint(
    'wordfrequency',
    __name__,
    url_prefix='/',
    static_url_path='',
    static_folder=''
    )

ALLOWED_EXTENSIONS = {'.txt', '.docx', '.doc'}

@wordfrequency_bp.route("/word-frequency", methods=['GET', 'POST'])
def word_frequency_page():
    if request.method == 'POST':
        response_dict = handle_word_count_request(request)
        return render_template(
            'word-frequency.html', 
            word_count=response_dict['word_count'])

    return render_template('word-frequency.html')


def handle_word_count_request(_request: Request) -> dict:
    if _request.form.get('word-frequency-text'):
        word_count = wf_api.string_word_count(_request.form.get('input-text'))

    elif _request.form.get('word-frequency-file'):
        word_count = handle_file_word_count_request(_request)
    
    response_dict = {
        'word_count': word_count
    }
    return response_dict


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

    save_safe_files(uploaded_files_list, upload_dir)

    # for _file in uploaded_files_list:
    #     upload(_file)
    #     upload_path = Path(upload_dir.joinpath(_file.filename))
    #     _file.save(upload_path)
    #     uploaded_file_paths.append(upload_path)

    # word_count = wf_api.file_word_count(uploaded_file_paths)

    # return word_count