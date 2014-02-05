__author__ = 'mandrake'

from flask import Blueprint, render_template
from utils.utl_github import github_status_lock, github_status

routes = Blueprint('github', __name__, template_folder='templates')
prefix = '/github'
static_path = 'static/github'


@routes.route('/')
def root():
    github_status_lock.acquire(1)
    local = list(github_status)
    github_status_lock.release()

    return render_template('github.html', repos=local)


@routes.route('/static/<path:path>')
def static(path):
    print path
    return path