__author__ = 'mandrake'

from application import app
import config

# Importing routes
mods = [
    'rts_index',
    'rts_calendar',
    'rts_forum',
    'rts_github'
]

for mod in mods:
    q = __import__('routes.' + mod)
    m = getattr(q, mod)
    app.register_blueprint(m.routes, url_prefix=m.prefix)


#print app.url_map


if __name__ == '__main__':
    app.run(host=config.host, debug=config.debug)