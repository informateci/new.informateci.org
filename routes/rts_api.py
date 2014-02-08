from flask import Blueprint
from utils.generic import ok_resp, err_resp, out_format
from sources.di_unipi import parse_istanze_esame, parse_studenti_iscritti
#from utils.utl_github import github_status_lock, github_status


routes = Blueprint('api', __name__)
prefix = '/api'


@routes.route('/appelli/<course>/<year>', methods=['GET'])
@out_format
def appelli_api(course, year):
    return ok_resp(data=parse_istanze_esame(course, year))

'''
@routes.route('/appelli/<course>/<year>/<exam>/<session>', methods=['GET'])
@out_format
def students_api(course, year, exam, session):
    return ok_resp(data=parse_studenti_iscritti(course, int(year), int(exam), int(session)))
'''

@routes.route('/appelli/iscritti/<listastud>')
@out_format
def students_api(listastud):
    return ok_resp(data=parse_studenti_iscritti(int(listastud)))

'''
@routes.route('/github', methods=['GET'])
@out_format
def github_api():
    github_status_lock.acquire(1)
    local = list(github_status)
    github_status_lock.release()
    return ok_resp(data=local)

'''
