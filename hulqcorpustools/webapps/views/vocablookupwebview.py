
from pathlib import Path

from flask import Blueprint, current_app, request, render_template

from ..plugins import vocablookupapi as vl_api

vocablookup_bp = Blueprint(
    'vocablookup',
    __name__,
    url_prefix='/vocab-lookup',
    static_url_path='',
    static_folder=''
    )


@vocablookup_bp.route("/", methods=['GET', 'POST'])
def vocab_lookup_page():

    if request.method == 'POST':
        with current_app.app_context():
            response = vl_api.handle_submission(
                request
                )

    else:
        response = ({}, 200)

    return render_template(
        'vocab-lookup.html',
        response=response[0],
        current_version=current_app.config["CURRENT_VERSION"])
