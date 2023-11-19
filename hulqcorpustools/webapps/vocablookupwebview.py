
from pathlib import Path

from flask import Blueprint, current_app, request, render_template, redirect, Request
from werkzeug.utils import secure_filename

from .plugins import vocablookupapi as vl_api


vocablookup_bp = Blueprint('vocablookup', __name__, url_prefix= '/', static_url_path='', static_folder='')

ALLOWED_EXTENSIONS = {'.txt', '.docx', '.doc'}

@vocablookup_bp.route("/vocab-lookup", methods=['GET', 'POST'])
def vocab_lookup_page():
    UPLOADS_FOLDER = current_app.config['UPLOADS_FOLDER']
    upload_dir = Path(UPLOADS_FOLDER)
    request # type: Request
    if request.method == 'POST':
        vocab_lookup = vl_api.handle_submission(
            request,
            upload_dir=upload_dir)

    else:
        vocab_lookup=""
    
    return render_template('vocab-lookup.html', vocab_lookup=vocab_lookup)
