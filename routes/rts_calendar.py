__author__ = 'mandrake'

from flask import Blueprint, render_template

routes = Blueprint('calendar', __name__, template_folder='templates')
prefix = '/calendar'


@routes.route('/')
def root():
    return render_template('calendar.html')