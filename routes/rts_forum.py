__author__ = 'mandrake'

from flask import Blueprint, render_template, redirect, url_for

routes = Blueprint('forum', __name__, template_folder='../templates/forum')
prefix = '/forum'


@routes.route('/')
def root():
    return redirect(url_for('.topics'))


@routes.route('/topics/', defaults={'page': '1'})
@routes.route('/topics/<page>')
def topics(page):
    return render_template('topics.html')


@routes.route('/thread/<id>')
def thread(id):
    return 'Roggan ' + str(id)


@routes.route('/message/<id>')
def message(id):
    return 'Roggan ' + str(id)


@routes.route('/pms/')
def pms():
    return render_template('privmsg.html')


@routes.route('/pms/<idnum>')
def pms_id(idnum):
    return 'Roggan ' + idnum


@routes.route('/news')
def news():
    return render_template('news.html')


@routes.route('/profile')
def profile():
    return render_template('profile.html')