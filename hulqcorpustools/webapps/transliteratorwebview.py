from pathlib import Path

from flask import Blueprint, current_app, request, render_template, url_for, redirect, send_from_directory
from flask.wrappers import Request, Response
from werkzeug.utils import secure_filename

from .plugins import transliteratorapi as tr_api

transliterator_bp = Blueprint('transliterator', __name__, url_prefix = '/', static_url_path='', static_folder='')

ALLOWED_EXTENSIONS = {'.txt', '.docx', '.doc'}

@transliterator_bp.route("/transliterator", methods=['GET', 'POST'])
def transliterator_page():

    anchor = ""
    transliterator_form = request.form
    source_formats = [
            {'name': 'Practical Orthography', 'value': 'Orthography'},
            {'name': 'APA Unicode', 'value': 'APA Unicode'},
            {'name': 'Straight', 'value': 'Straight'}]
    target_formats = [
            {'name': 'APA Unicode', 'value': 'APA Unicode'},
            {'name': 'Practical Orthography', 'value': 'Orthography'}]

    if request.method == 'POST':

        if request.form.get('string-transliterate'):
            transliterator_response = string_transliterate(request)

        elif request.form.get('upload-transliterate'):
            transliterator_response = file_transliterate(request)
        
        if type(transliterator_response) == Response:
            ...

        else:
            transliterator_form = transliterator_response


    return render_template(
        'transliterator.html',
        transliterator_form=transliterator_form,
        source_formats=source_formats,
        target_formats=target_formats,
        anchor=anchor
        )


def string_transliterate(request):
    input_text = request.form['input-text']
    source_format = request.form['source-format-selection']
    target_format = request.form['target-format-selection']
    
    transliterated_text = tr_api.transliterate_string(
    input_text,
    source_format,
    target_format
    )

    transliterator_form = {
        'input': input_text,
        'source_format': source_format,
        'target_format': target_format,
        'output': transliterated_text
    }

    return transliterator_form

def file_transliterate(request: Request):
    uploaded_files_list = request.files.getlist('transliterate-files')
    source_format = request.form['source-format-selection']
    target_format = request.form['target-format-selection']

    if request.form.get('font-search-transliterate'):
        font_search = True
    else:
        font_search = None

    transliterator_form = request.form

    if uploaded_files_list[0].filename == '':
        return redirect(request.url)

    ...
    for _file in uploaded_files_list:
        _file.filename = secure_filename(_file.filename)

    uploaded_files_list = [_file for _file in uploaded_files_list if Path(_file.filename).suffix in ALLOWED_EXTENSIONS]

    UPLOAD_FOLDER = current_app.config['UPLOAD_FOLDER']
    upload_dir = Path(UPLOAD_FOLDER)

    uploaded_file_paths = []

    for i in uploaded_files_list:
        upload_path = Path(upload_dir.joinpath(i.filename))
        i.save(upload_path)
        uploaded_file_paths.append(upload_path)
    

    transliterated_files = tr_api.transliterate_file_list(
        uploaded_file_paths,
        source_format,
        target_format,
        font_search=font_search
        )
    
    print(transliterated_files)

    transliterated_file_form = {
        'source_format': source_format,
        'target_format': target_format,
        'font_search': font_search,
        'transliterated_files': transliterated_files
    }

    return transliterated_file_form

@transliterator_bp.route("/uploads/<filename>", methods=['GET', 'POST'])
def download_transliterated_file(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename, as_attachment=True)


def allowed_file(file):
    filename = Path(file.filename)
    if filename.suffix in ALLOWED_EXTENSIONS:
        return True
    else:
        return False