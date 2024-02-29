from pathlib import Path

from flask import (
    Blueprint,
    current_app,
    request,
    render_template,
    # url_for,
    redirect,
    send_from_directory
    )
from flask.wrappers import Request, Response

from hulqcorpustools.resources.constants import TextFormat

from ..plugins import transliteratorapi as tr_api

transliterator_bp = Blueprint(
    'transliterator',
    __name__,
    url_prefix='/',
    static_url_path='',
    static_folder=''
    )

ALLOWED_EXTENSIONS = {'.txt', '.docx', '.doc'}

display_keys = {
    TextFormat("orthography"): "Practical Orthography",
    TextFormat("apaunicode"): "APA Unicode",
    TextFormat("straight"): "Straight"
}

@transliterator_bp.route("/transliterator", methods=['GET', 'POST'])
def transliterator_page():
    current_version = current_app.config['CURRENT_VERSION']
    anchor = ""
    transliterator_form = request.form
    source_formats = display_keys
    target_formats = display_keys
    
    if request.method == 'POST':

        if request.form.get('string-transliterate'):
            transliterator_response = string_transliterate(request)

        elif request.form.get('upload-transliterate'):
            transliterator_response = file_transliterate(request)

        if isinstance(transliterator_response, Response):
            ...

        else:
            transliterator_form = transliterator_response

    return render_template(
        'transliterator.html',
        transliterator_form=transliterator_form,
        source_formats=source_formats,
        target_formats=target_formats,
        anchor=anchor,
        current_version=current_version,
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
        'input_text': input_text,
        'source_format': source_format,
        'target_format': target_format,
        'output': transliterated_text
    }

    return transliterator_form


def file_transliterate(request: Request):
    uploaded_files_list = request.files.getlist('transliterate-files')
    source_format = request.form['source-format-selection']
    target_format = request.form['target-format-selection']

    if uploaded_files_list[0].filename == '':
        return redirect(request.url)

    search_method = request.form.get("font-search-selection")

    transliterated_files = tr_api.transliterate_file_list(
        uploaded_files_list,
        source_format,
        target_format,
        font=search_method
        )

    transliterated_file_form = {
        'source_format': source_format,
        'target_format': target_format,
        'font_search': search_method,
        'transliterated_files': transliterated_files
    }

    return transliterated_file_form


@transliterator_bp.route("/uploads/<filename>", methods=['GET', 'POST'])
def download_transliterated_file(filename):
    return send_from_directory(
        current_app.config['UPLOADS_FOLDER'],
        filename,
        as_attachment=True
        )

