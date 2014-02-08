from flask import Blueprint
from utils.generic import ok_resp, err_resp, out_format
from utils.utl_calendar import calendar_status, calendar_status_lock
#from utils.utl_github import github_status_lock, github_status


routes = Blueprint('api', __name__)
prefix = '/api'


@routes.route('/appelli', methods=['GET'])
@out_format
def appelli_api():
    calendar_status_lock.acquire(1)
    local = list(calendar_status)
    calendar_status_lock.release()
    return ok_resp(data=local)

'''
@routes.route('/github', methods=['GET'])
@out_format
def github_api():
    github_status_lock.acquire(1)
    local = list(github_status)
    github_status_lock.release()
    return ok_resp(data=local)

'''
