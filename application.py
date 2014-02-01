__author__ = 'mandrake'
from flask import Flask

app = Flask(__name__)

mods = [
    'rts_calendar',
    'rts_forum',
    'rts_github',
    'rts_index'
]

for mod in mods:
    q = __import__('routes.' + mod)
    m = getattr(q, mod)
    app.register_blueprint(m.routes, url_prefix=m.prefix)

if __name__ == '__main__':
    app.run(debug=True)