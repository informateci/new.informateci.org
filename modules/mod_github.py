__author__ = 'mandrake'

from github import MainClass
from secure import SECURE

github_obj = MainClass.Github(client_id=SECURE['client_id'], client_secret=SECURE['client_secret'])