__author__ = 'mandrake'
from flask import Flask

app = Flask(__name__)

from routes.routes import bprint
app.register_blueprint(bprint)

if __name__ == '__main__':
    app.run(debug=True)