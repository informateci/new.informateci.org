__author__ = 'mandrake'

from github import MainClass
from secure import SECURE
from threading import Event, Thread, RLock
import pickle
import os.path

task_kill = Event()
github_status = []
github_status_lock = RLock()
CACHE_FILE = './cache/github_status'

class GithubCacheRepo():
    def __init__(self, name='', desc='', comms=None):
        self.name = name
        self.description = desc
        self.commits = comms

    def get_commits(self):
        return self.commits


class GithubCacheCommit():
    def __init__(self, name='', desc='', sha='', auth=''):
        self.name = name
        self.description = desc
        self.sha = sha
        self.short_sha = sha[-8:] if sha != '' else ''
        self.author = auth


class GithubThread(Thread):
    def __init__(self, event):
        global github_status

        Thread.__init__(self)
        self.event = event
        if os.path.isfile(CACHE_FILE):
            f = open(CACHE_FILE, 'rb')
            github_status = pickle.load(f)
            f.close()
        else:
            GithubThread.rifrescia()

    @staticmethod
    def rifrescia():
        global github_status
        github_obj = MainClass.Github(client_id=SECURE['client_id'], client_secret=SECURE['client_secret'])
        repos = github_obj.get_user('informateci').get_repos()
        status = list()
        for repo in repos:
            comms = []
            for commit in repo.get_commits():
                comms.append(GithubCacheCommit(sha=commit.sha))
            status.append(GithubCacheRepo(name=repo.name, desc=repo.description, comms=comms))

        f = open(CACHE_FILE, 'wb')
        github_status_lock.acquire(1)
        github_status = status
        pickle.dump(github_status, f)
        github_status_lock.release()
        f.close()

    def run(self):
        while not self.event.wait(300):
            GithubThread.rifrescia()


github_thread = GithubThread(task_kill)
github_thread.start()

def github_stop():
    task_kill.set()