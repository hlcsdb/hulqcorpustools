
from flask import (
    Blueprint,
    current_app,
    request,
    render_template,
)

from ..plugins import wordfrequencyapi as wf_api

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
        response = wf_api.handle_request(request)

    else:
        response = ({}, 200)

    return render_template(
        'word-frequency.html',
        word_count=response[0].get("word_count"),
        current_version=current_app.config.get("CURRENT_VERSION")
    )