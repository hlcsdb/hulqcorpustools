
import logging
from logging.config import dictConfig
import os
from pathlib import Path
from dotenv import load_dotenv

from flask import Flask, render_template

from .views import transliteratorwebview, wordfrequencywebview, vocablookupwebview

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

app = Flask(__name__)
current_version = importlib.metadata.version('hulqcorpustools')

app.config['UPLOADS'] = os.environ.get('UPLOADS')


app.config['CURRENT_VERSION'] = importlib.metadata.version('hulqcorpustools')
# if transliterator folder not put in env: use root path of app
if app.config == None:
    app.config['UPLOADS_FOLDER'] = app.root_path + "/uploads/"
    if Path(app.config).exists is False:
        Path(app.config).mkdir()


@app.route("/", methods=['GET', 'POST'])
def index():

    return render_template(
        'index.html'
        )


with app.app_context():
    app.register_blueprint(transliteratorwebview.transliterator_bp)
    app.register_blueprint(wordfrequencywebview.wordfrequency_bp)
    app.register_blueprint(vocablookupwebview.vocablookup_bp)


if __name__ == "__main__":
    app.run(host='0.0.0.0')
