#!/usr/bin/python3
""" rendering html showing states """
from flask import Flask, render_template
from models import storage
from models.state import State
from models.city import City


app = Flask(__name__)


@app.teardown_appcontext
def tear(exception):
    """ Tears down the session """
    storage.close()


@app.route('/states/', strict_slashes=False)
@app.route('/states/<id>', strict_slashes=False)
def state(id=None):
    """ Function display state and id """
    states = storage.all(State)

    if not id:
        dct = {value.id: value.name for value in states.values()}
        return render_template('7-states_list.html',
                               Table="States",
                               items=dct)

    i = "State.{}".format(id)
    if i in states:
        return render_template('9-states.html',
                               Table="State: {}".format(states[i].name),
                               items=states[i])

    return render_template('9-states.html',
                           items=None)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
