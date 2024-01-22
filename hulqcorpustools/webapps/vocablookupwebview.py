
from pathlib import Path

from flask import Blueprint, current_app, request, render_template, redirect, Request
from werkzeug.utils import secure_filename

from .plugins import vocablookupapi as vl_api

vocablookup_bp = Blueprint('vocablookup', __name__, url_prefix= '/vocab-lookup', static_url_path='', static_folder='')

ALLOWED_EXTENSIONS = {'.txt', '.docx', '.doc'}

@vocablookup_bp.route("/", methods=['GET', 'POST'])
def vocab_lookup_page():
    UPLOADS_FOLDER = current_app.config['UPLOADS_FOLDER']
    upload_dir = Path(UPLOADS_FOLDER)

    if request.method == 'POST':
        vocab_lookup_response = vl_api.handle_submission(
            request,
            upload_dir=upload_dir)
        print(vocab_lookup_response.get('file_list'))
    else:
        vocab_lookup_response=""
    
    return render_template('vocab-lookup.html', vocab_lookup_response=vocab_lookup_response)
