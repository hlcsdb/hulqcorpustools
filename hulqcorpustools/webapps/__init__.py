from importlib import metadata
from logging.config import dictConfig
from dotenv import dotenv_values

from flask import Flask, render_template, g
from hulqcorpustools.utils.keywordprocessors import kp
from hulqcorpustools.vocablookup.vocablookup import Vocab
from .views import (
    transliteratorwebview,
    wordfrequencywebview,
    vocablookupwebview
    )

def create_app(test_config=None):

    dictConfig({
        'version': 1,
        'formatters': {'default': {
            'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
        }},
        'handlers': {'wsgi': {
            'class': 'logging.StreamHandler',
            'stream': 'ext://flask.logging.wsgi_errors_stream',
            'formatter': 'default'
        }},
        'root': {
            'level': 'INFO',
            'handlers': ['wsgi']
        }
    })

    app = Flask(__name__)#, instance_relative_config=True)
    
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