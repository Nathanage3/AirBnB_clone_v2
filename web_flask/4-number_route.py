#!/usr/bin/python3
"""
Flask model
"""
from flask import Flask

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hbnb():
    """
    Route to display "Hello HBNB!"
    """
    return 'Hello HBNB!'


@app.route('/hbnb', strict_slashes=False)
def index():
    """
    Route to display "HBNB"
    """
    return 'HBNB'


@app.route('/c/<text>', strict_slashes=False)
def c_is(text):
    """
    Route to display "C is " followed by the value of the text variable.
    Replace underscore (_) symbols with a space.
    """
    return 'C is {:s}'.format(text.replace('_', ' '))


@app.route('/python/', defaults={'text': 'is cool'}, strict_slashes=False)
@app.route('/python/<text>')
def python(text):
    """
    Route to display "Python " followed by the value of the text variable.
    Replace underscore (_) symbols with a space.
    """
    return 'Python {:s}'.format(text.replace('_', ' '))


@app.route('/number/<int:n>', strict_slashes=False)
def number(n):
    """
    Route to display "{} is a number".
    """
    return '{} is a number'.format(n)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
