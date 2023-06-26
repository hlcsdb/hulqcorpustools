
import logging
from flask import Flask, render_template, url_for
from markupsafe import escape

app = Flask(__name__)

app.config["APPLICATION_ROOT"] = "/apps"

@app.route("/", methods=['GET', 'POST'])
def index():

    return render_template(
        'index.html'
        )

@app.route("/fun")
def fun_page():
    fun_js = url_for('static', filename='scripts/main.js')
    print(fun_js)
    return render_template('fun.html', fun_js=fun_js)

from . import onlinetransliterator
app.register_blueprint(onlinetransliterator.bp)

if __name__ == "__main__":
    app.run(host='0.0.0.0')

