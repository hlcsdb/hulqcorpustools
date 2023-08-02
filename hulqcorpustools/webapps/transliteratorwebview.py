from pathlib import Path

from flask import Blueprint, current_app, request, render_template, url_for, redirect, send_from_directory
from werkzeug.utils import secure_filename

from .plugins.transliteratorwebcontroller import _transliterate_string, _transliterate_file

transliterator_bp = Blueprint('transliterator', __name__, url_prefix = '/', static_url_path='', static_folder='')

ALLOWED_EXTENSIONS = {'.txt', '.docx'}

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
        
        if 'string-transliterate' in request.form:
            transliterator_form = string_transliterate(request)

        if 'upload-transliterator-files' in request.form:
            transliterator_form = file_transliterate(request)

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
    
    transliterated_text = _transliterate_string(
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

def file_transliterate(request):
    source_format = request.form['source-format-selection']
    target_format = request.form['target-format-selection']

    if 'transliterate-file' not in request.files:
        return redirect(request.url)

    file = request.files['transliterate-file']

    if allowed_file(file) is False:
        return redirect(request.url)

    filename = secure_filename(file.filename)
    UPLOAD_FOLDER = current_app.config['UPLOAD_FOLDER']
    upload_dir = Path(UPLOAD_FOLDER)
    upload_path = upload_dir.joinpath(filename)
    file.save(upload_path)
    
    transliterated_files = _transliterate_file(
        upload_path,
        source_format,
        target_format
        )
    

    transliterated_file_form = {
        'source_format': source_format,
        'target_format': target_format,
        'transliterated_docx': transliterated_files.get('transliterated_docx'),
        'transliterated_txt': transliterated_files.get('transliterated_txt')
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