#!/usr/bin/python3
""" rendering html showing states of the module"""
from flask import Flask, render_template
from models import storage
from models.state import State


app = Flask(__name__)


@app.teardown_appcontext
def tear(exception):
    """ Tears down the session """
    storage.close()


@app.route('/states_list', strict_slashes=False)
def states():
    """ Function called with /states_list route """
    states = storage.all(State)
    dct = {value.id: value.name for value in states.values()}
    return render_template('7-states_list.html',
                           Table="States",
                           items=dct)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
