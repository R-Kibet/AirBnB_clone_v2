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
    return "C " + str(text.replace('_', ' '))


@app.route('/python', strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def frth(text="is cool"):
    """ adding a default """
    if text != "is cool":
        return "Python " + str(text.replace('_', ' '))
    return "Python " + str(text)


@app.route('/number/<int:n>', strict_slashes=False)
def fth(n):
    """ display n if only int """
    return "%d is a number" % n


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
