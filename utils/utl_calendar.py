__author__ = 'mandrake'

from threading import Thread, Event, RLock
from sources.calendar.web_unipi import parse_exam_names, WebUnipi
import os
import pickle


task_kill = Event()
calendar_status = []
calendar_status_lock = RLock()
CACHE_FILE = './cache/calendar_status'


class CalendarThread(Thread):
    def __init__(self, event):
        global calendar_status

        Thread.__init__(self)
        self.event = event
        if os.path.isfile(CACHE_FILE):
            f = open(CACHE_FILE, 'rb')
            calendar_status = pickle.load(f)
            f.close()
        else:
            CalendarThread.rifrescia()

    @staticmethod
    def rifrescia():
        global calendar_status

        q = WebUnipi()
        status = q.get_appelli()
        f = open(CACHE_FILE, 'wb')
        calendar_status_lock.acquire(1)
        calendar_status = status
        pickle.dump(calendar_status, f)
        calendar_status_lock.release()
        f.close()

    def run(self):
        while not self.event.wait(3600):
            CalendarThread.rifrescia()

calendar_thread = CalendarThread(task_kill)
calendar_thread.start()

def calendar_stop():
    task_kill.set()