from pathlib import Path

from flask import (
    Blueprint,
    current_app,
    g,
    request,
    render_template,
    send_from_directory
    )

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

source_display_keys = {
    TextFormat("orthography"): "Practical Orthography",
    TextFormat("apaunicode"): "APA Unicode",
    TextFormat("straight"): "Straight"
}
target_display_keys = {
    TextFormat("orthography"): "Practical Orthography",
    TextFormat("apaunicode"): "APA Unicode",
}

@transliterator_bp.route("/transliterator", methods=['GET', 'POST'])
def transliterator_page():
    anchor = ""
    source_formats = source_display_keys
    target_formats = target_display_keys
    if request.method == 'POST':
        with current_app.app_context():
            response = tr_api.request_handler(request)
    else:
        response = ({}, 200)
    return render_template(
        'transliterator.html',
        response=response[0],
        source_formats=source_formats,
        target_formats=target_formats,
        anchor=anchor,
        current_version=current_app.config['CURRENT_VERSION']
        )

@transliterator_bp.route("/uploads/<file>", methods=['GET', 'POST'])
def download_file(file: str) -> str:
    """Generate download link for a file, rendering it
    relative to upload folder if needed

    Args:
        file (tuple[str, str]): tuple of strs [filename, url]

    Returns:
        str: appropriate url to download file
    """
    return send_from_directory(
            current_app.config.get("UPLOADS"),
            file,
            as_attachment=True)
