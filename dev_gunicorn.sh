#!/bin/sh 

echo "---\nstarting gunicorn now ...\n"
# only works if gunicorn is installed a local venv, where that venv is called 'venv'
gunicorn --conf './gunicorn_conf.py' 'hulqcorpustools.webapps.app:app'
