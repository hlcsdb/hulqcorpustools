
import importlib
import logging
import os
from pathlib import Path
from dotenv import load_dotenv

from flask import Flask, render_template

from .views import transliteratorwebview, wordfrequencywebview, vocablookupwebview


app = Flask(__name__)


current_version = importlib.metadata.version('hulqcorpustools')
app.config['UPLOADS'] = os.environ.get('UPLOADS')
app.config['CURRENT_VERSION'] = importlib.metadata.version('hulqcorpustools')
# if transliterator folder not put in env: use root path of app
if app.config == None:
    app.config['UPLOADS_FOLDER'] = app.root_path + "/uploads/"
    if Path(app.config).exists is False:
        Path(app.config).mkdir()

gunicorn_logger = logging.getLogger("gunicorn.error")
app.logger.handlers = gunicorn_logger.handlers
app.logger.setLevel(gunicorn_logger.level)
app.logger.info("gunicorn started")

print("hmm")
app.logger.debug("debug")
app.logger.critical("oh no")

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
