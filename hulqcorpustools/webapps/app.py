
import os
from pathlib import Path

from flask import Flask, render_template, url_for
from markupsafe import escape

app = Flask(__name__)

app.config['UPLOADS_FOLDER'] = os.environ.get('UPLOADS_FOLDER')
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

from . import transliteratorwebview, wordfrequencywebview
app.register_blueprint(transliteratorwebview.transliterator_bp)
app.register_blueprint(wordfrequencywebview.wordfrequency_bp)

if __name__ == "__main__":
    app.run(host='0.0.0.0')


