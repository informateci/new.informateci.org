__author__ = 'mandrake'

from github import MainClass
from application import app
from secure import SECURE

gitubbo = MainClass.Github(client_id=SECURE['client_id'], client_secret=SECURE['client_secret'])

@app.route('/github')
def gitubbo():
    return gitubbo.get_user('informateci').get_repos()