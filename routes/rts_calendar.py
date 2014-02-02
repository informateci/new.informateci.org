__author__ = 'mandrake'

from flask import Blueprint, render_template, send_from_directory

routes = Blueprint('calendar', __name__, template_folder='templates')
prefix = '/calendar'
static_path = 'static/calendar'


@routes.route('/')
def root():
    return render_template('calendar/index-bs3.html')


@routes.route('/static/<path:path>')
def js(path):
    return send_from_directory(static_path, path)