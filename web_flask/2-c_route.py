#!/usr/bin/python3
""" starts a Flask web application """

from flask import Flask


app = Flask(__name__)


@app.route('/', strict_slashes=False)
def start():
    """ function display hello """
    return "Hello HBNB!"


@app.route('/hbnb', strict_slashes=False)
def scnd():
    """ display secnd route """
    return "HBNB"


@app.route('/c/<text>', strict_slashes=False)
def thrd(text):
    """ using rule in route """
    return "C " + str(text)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
