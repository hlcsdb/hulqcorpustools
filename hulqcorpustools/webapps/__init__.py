from importlib import metadata
import json
import logging
import os
from pathlib import Path

import boto3
import dotenv
from flask import Flask, render_template
from werkzeug.middleware.profiler import ProfilerMiddleware

from hulqcorpustools.vocablookup.vocablookup import Vocab
from hulqcorpustools.webapps.plugins.common import Upload
from hulqcorpustools.webapps.views import (
    transliteratorwebview,
    wordfrequencywebview,
    vocablookupwebview
    )


def get_upload(
        ):

    _upload_config = os.getenv("UPLOAD")
    if _upload_config == "s3":
        dotenv.load_dotenv(os.getenv("SECRETS"))
        _upload = boto3.client(
            "s3",
            aws_access_key_id=os.getenv("S3_BUCKET_ACCESS_KEY"),
            aws_secret_access_key=os.getenv("S3_BUCKET_SECRET_KEY"),
            endpoint_url=os.getenv("S3_DOMAIN"),
            )
        
        return Upload(
            _upload,
            upload_bucket=os.getenv("S3_BUCKET_NAME")
            )
        # _upload = _upload_server.Bucket(os.getenv("S3_BUCKET_NAME"))

    else:
        try:
            _upload_path = Path(_upload_config)
            if _upload_path.exists():
                return Upload(_upload_path)
        except TypeError as e:
            return e

    return Upload(_upload)

def create_app(test_config=None):

    dotenv.load_dotenv(os.getenv("SECRETS"))
    app = Flask(__name__)#, instance_relative_config=True)

    if os.getenv("LOGGER") == "gunicorn":
        gunicorn_logger = logging.getLogger("gunicorn.error")
        app.logger.handlers = gunicorn_logger.handlers
        app.logger.setLevel(gunicorn_logger)
        app.logger.info("gunicorn started")

    if os.getenv("PROFILE") == "True":
        app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions=[30])
        
    app.config.from_file(os.getenv("CONFIG_JSON"), load=json.load)
    app.config["CURRENT_VERSION"] = metadata.version
    # app.logger.debug(f"app config:\n{app.config}")

    with app.app_context():
        app.upload = get_upload()

        if not isinstance(app.upload, Upload):
            app.logger.error("Error with configuring uploads.")
        app.vocab_db = Vocab(app.config.get("VOCAB_DB"))
        app.register_blueprint(transliteratorwebview.transliterator_bp)
        app.register_blueprint(wordfrequencywebview.wordfrequency_bp)
        app.register_blueprint(vocablookupwebview.vocablookup_bp)

        @app.route("/", methods=["GET", "POST"])
        def index():
            return render_template(
                "index.html"
            )

    return app