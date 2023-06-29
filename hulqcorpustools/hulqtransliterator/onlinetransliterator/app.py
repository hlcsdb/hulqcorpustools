
import os
from pathlib import Path

from flask import Flask, render_template, url_for
from markupsafe import escape

app = Flask(__name__)

app.config['APPLICATION_ROOT'] = '/apps'
app.config['UPLOAD_FOLDER'] = os.environ.get('TRANSLITERATOR_UPLOADS_FOLDER')

# if transliterator folder not put in env: use root path of app
if app.config == None:
    app.config['UPLOAD_FOLDER'] = app.root_path + "/uploads/"
    if Path(app.config).exists is False:
        Path(app.config).mkdir() 

@app.route("/", methods=['GET', 'POST'])
def index():

    return render_template(
        'index.html'
        )

from . import onlinetransliterator
app.register_blueprint(onlinetransliterator.bp)

if __name__ == "__main__":
    app.run(host='0.0.0.0')

