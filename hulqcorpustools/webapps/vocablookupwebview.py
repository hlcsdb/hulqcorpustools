
from pathlib import Path

from flask import Blueprint, current_app, request, render_template, redirect, Request
from werkzeug.utils import secure_filename

from hulqcorpustools.webapps.plugins import vocablookupapi


vocablookup_bp = Blueprint('vocablookup', __name__, url_prefix= '/', static_url_path='', static_folder='')

ALLOWED_EXTENSIONS = {'.txt', '.docx'}

@vocablookup_bp.route("/vocab-lookup", methods=['GET', 'POST'])
def vocab_lookup_page():
    request # type: Request
    if request.method == 'POST':
        vocab_lookup = vocablookupapi.handle_submission(request)
        for i, j in vocab_lookup['vocab_found'].items():
            print(i, j)
    else:
        vocab_lookup=""
    
    return render_template('vocab-lookup.html', vocab_lookup=vocab_lookup)
