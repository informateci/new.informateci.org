__author__ = 'mandrake'

from application import app, login_manager
import config
import signal
import os
import gevent
from gevent.wsgi import WSGIServer

PATH = os.path.dirname(__file__)





# Importing routes
mods = [
    'rts_index',
    'rts_calendar',
    'rts_api'
    #'rts_forum',
    #'rts_github'
]

for mod in mods:
    q = __import__('routes.' + mod)
    m = getattr(q, mod)
    app.register_blueprint(m.routes, url_prefix=m.prefix)


#print app.url_map

app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'


if __name__ == '__main__':

    gevent.signal(signal.SIGQUIT, gevent.shutdown)
    http_server = WSGIServer((config.host, config.port), app)
    try:
        http_server.serve_forever()
    except KeyboardInterrupt:
        print "FINISH"
        http_server.stop()
        print "ENDE"
        # la morte
        pid = os.getpid()
        os.kill(pid, 1)