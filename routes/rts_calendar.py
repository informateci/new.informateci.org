from sources.di_unipi import parse_istanze_esame

__author__ = 'mandrake'

from flask import Blueprint, render_template, send_from_directory

routes = Blueprint('calendar', __name__, template_folder='templates')
prefix = '/calendar'
static_path = 'static/calendar'


@routes.route('/')
def root():
    return render_template('calendar/index-bs3.html')


@routes.route('/appelli')
def appelli():
    return render_template('stub.html', data=parse_istanze_esame('inf31', 2014))


@routes.route('/appelli/<anno>')
def appcazzy(anno):
    return render_template('stub.html', data=parse_istanze_esame('inf31', int(anno)))

'''
@routes.route('/appelli/<anno>/<corso>/<idesame>/<idappello>')
def iscritti(corso, anno, idesame, idappello):
    return render_template('stub.html', data=parse_students(corso, int(anno), int(idesame), idappello))
'''

@routes.route('/static/<path:path>')
def static(path):
    print static_path, path
    return send_from_directory(static_path, path)