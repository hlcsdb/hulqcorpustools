from flask import Blueprint, Flask, request, render_template, url_for, redirect

from .plugins.webtransliterator import web_transliterate_string

bp = Blueprint('onlinetransliterator', __name__, url_prefix = '/')

@bp.route("/transliterator", methods=['GET', 'POST'])
def transliterator():

    transliterator_form = request.form

    source_formats = [
            {'name': 'Straight', 'value': 'Straight'},
            {'name': 'APA Unicode', 'value': 'APA Unicode'},
            {'name': 'Practical Orthography', 'value': 'Orthography'}]
    target_formats = [
            {'name': 'APA Unicode', 'value': 'APA Unicode'},
            {'name': 'Practical Orthography', 'value': 'Orthography'}]

    if request.method == 'POST':
        transliterator_input_text = request.form['input-text']
        
        selected_source_format = request.form['source-format-selection']
        selected_target_format = request.form['target-format-selection']
        
        transliterator_output_text = web_transliterate_string(transliterator_input_text, selected_source_format, selected_target_format)
        
        transliterator_form = \
            {'input': transliterator_input_text,
             'source_format': selected_source_format,
             'target_format': selected_target_format,
             'output': transliterator_output_text}

    return render_template('transliterator.html',
        transliterator_form=transliterator_form,
        source_formats=source_formats,
        target_formats=target_formats)