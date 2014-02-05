from sources.calendar.web_unipi import parse_students, WebUnipi

__author__ = 'mandrake'

from flask import Blueprint, render_template, send_from_directory
from utils.utl_calendar import calendar_status, calendar_status_lock

routes = Blueprint('calendar', __name__, template_folder='templates')
prefix = '/calendar'
static_path = 'static/calendar'


@routes.route('/')
def root():
    return render_template('calendar/index-bs3.html')


@routes.route('/appelli')
def appelli():
    calendar_status_lock.acquire(1)
    local = list(calendar_status)
    calendar_status_lock.release()
    return render_template('stub.html', data=local)


@routes.route('/appelli/<anno>')
def appcazzy(anno):
    w = WebUnipi()
    return render_template('stub.html', data=w.get_appelli(int(anno)))


@routes.route('/appelli/<anno>/<corso>/<idesame>/<idappello>')
def iscritti(corso, anno, idesame, idappello):
    return render_template('stub.html', data=parse_students(corso, int(anno), int(idesame), idappello))


@routes.route('/static/<path:path>')
def static(path):
    print static_path, path
    return send_from_directory(static_path, path)