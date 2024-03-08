from importlib import metadata
import logging
from dotenv import dotenv_values

from flask import Flask, render_template
from hulqcorpustools.vocablookup.vocablookup import Vocab
from .views import (
    transliteratorwebview,
    wordfrequencywebview,
    vocablookupwebview
    )

def create_app(test_config=None):

    app = Flask(__name__)#, instance_relative_config=True)
    gunicorn_logger = logging.getLogger("gunicorn.error")
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.info("gunicorn started")
    
    for env_key, env_value in dotenv_values().items():
        app.config[env_key] = env_value
    app.config["CURRENT_VERSION"] = metadata.version

    @app.route("/", methods=["GET", "POST"])
    def index():
        return render_template(
            "index.html"
        )
    
    with app.app_context():
        app.vocab_db = Vocab(app.config["VOCAB_DB"])
        app.register_blueprint(transliteratorwebview.transliterator_bp)
        app.register_blueprint(wordfrequencywebview.wordfrequency_bp)
        app.register_blueprint(vocablookupwebview.vocablookup_bp)


    return app