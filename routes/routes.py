__author__ = 'mandrake'
from flask import render_template, Response, Blueprint
import base64
from modules.mod_github import github_status, github_status_lock
from copy import deepcopy

bprint = Blueprint('bprint', __name__, template_folder='templates')


@bprint.route('/')
def index_route():
    return render_template('index.html')


@bprint.route('/favicon.ico')
def favicon_route():
    return Response(
        base64.decodestring('iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAAGXRFWHRTb\
        2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAABOtJREFUeNrkV81rXUUUPzP3vveSvEBS41P8boh\
        SqC6iKbiooLhxpWSrO8E/oCtFLbhyIbQYUEFx4cY/oN246qJ140KFSAWtoJuAUoWatMnLzf2Y4zlnP\
        u5M733ZduENk5k3M3fOb875nd/MVYgI9/LRcI+f3DeUUnD29c+XAHELATepaxnEO2gr8G3nMT8Wt/2\
        8njF6dundS1Sf++Hyu3t+HeUbL7zxBRu/OjfK19ceX4H5uYGDRgsZEMOGi0FojAl1w3Vj2uJ+11Eft\
        +u6guJwSms127TaS99ffm8v8QDvnI2f3TgJw0FOHrFe8SDIFpXUYF3bxatQN9LHNZeS+6sGFLWV1lQ\
        yONzfWzdotmjRNxMOsNuffOJ+GA1zyLSCPNNSBrmGYZ5Rf0bAbOG+nPoyqjOak+VK3uGiuTjwqt0dt\
        VE2lQ9GvNnNDgc45gvzA3lZu4V4QVnIrWQrcj8Z1RQXHjdU9nYLuHNQgvEh4BA1LkQNc8MIAA6jW2u\
        5C4AGV5YXxIx3f1ssBxiBCkAA9qclXP/tJry48RCcOb0qbtaKwbO72RNa+j747FsYZExOAkJ9cepHH\
        kBH1qRHgPF8Jp0QzxGRF/n1j3/g/bc2YO2xE7C4uAij0SiA7iyEPoNCVqQAEP08biiphf3QZgC70wO\
        5vV/A+qkVMT6ZTGA4HMrOE7sC1rgUNeIBxHSjOoYpRjnKDq0YNT6l2phy/fetA3L7gzAej8V4nucCI\
        C5ZlgVQ6D0gNmaEgA0qgwl77Tso5AppaKx3xgtDcTsb8s83127AR19eExJ7o8p5wG7QzAqB27WxTMX\
        Gsg1NLEAOhMt5TzjLbgv706+/gwfum6c5pAVVTfOoVFYfbBjSEMRpCDt/3ZZdLczllOs25zExjkGIG\
        NQzT03EcBz7o7KC8bwWoNZjHEIG0EhtTNPvAUZWElJD5JoeanEh/3lNkPSjf00AgTbd7mI8j+1PC1H\
        AsqrEU6apBUwIw6w0ZLScpyI2xqYT1hhemhaVFH6/OKoC2RIABOywMC5btEWtOaRHgYT9HACb64SX5\
        iiJb5vCFsDBtILNl9dg9dElEZk+D1x4+xWrmk6Uft+5BR9/dTXEX+q+45gHWUpZAwyqoOWWMxjIeGp\
        1As89/YgwnwunX/w8v37S5b5V059u3KTdV60QBS/0hKAmI5oV12WCkgRKj2I2GOd97y0n6t/+5U8KS\
        +nibuxmZimhEMUJvkpUFJ0WGKvxPbGf9fz4845zu1dBMysNLbNlVMXHgxMjY+t3Ll6x4aL2J+dfhWd\
        PP5wYpFsVXzoC0Zr6KHE/ziIhuB3GZxJiq4TGvUjyIGBY0Mqy7OyYjVdHdxLSJQQ8VoqN3ZlHKmHBN\
        g3lRZfPTFS5HdDvNBx4l3GM2O+kuC8E6ESkleR254jdRZU763ufaL6cgNGF9tgQeNkVowaT3UNQMXu\
        sgrZa0Tn7/ZEe+I7RMWw6aZgcx1VVth6IXR8Zx6hf9QhRSLfIYELA4JHuh8kun2DGhjmQL4lh5AkvN\
        P0RwIhHvQTc7QDgj4aymLpDIyZQSqSwM4jvDcdxoL0D2FrGL/V54Bx/NBQH/9JJVpAsV0nsQhaEuM7\
        6pox3a8Lc6Itqm22FL7L4MnHmtQ+XaOqWu7cvB8YiBOPuppqy2YPzY1E7cbv7NLt+5UL30+x/+3X8n\
        wADAGdc48ttRnltAAAAAElFTkSuQmCC'),
        mimetype='image/png'
    )


@bprint.route('/github')
def github_route():
    local = []
    github_status_lock.acquire(1)
    local = list(github_status)
    github_status_lock.release()
    ret = render_template('github.html', repos=local)
    return ret