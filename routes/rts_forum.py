__author__ = 'mandrake'

from flask import Blueprint

routes = Blueprint('forum', __name__, template_folder='templates')
prefix = '/forum'