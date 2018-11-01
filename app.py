#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, make_response, render_template
from flask_bootstrap import Bootstrap
app = Flask(__name__)
bootstrap = Bootstrap(app)


@app.route('/')
def index():
    response = make_response(render_template('index.html'))
    return response


@app.route('/user/<name>')
def user(name):
    response = make_response(render_template('user.html', name=name))
    return response


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


if __name__ == '__main__':
    app.run(debug=True)
