#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, make_response, render_template, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
app = Flask(__name__)
app.config['CSRF_ENABLED'] = True
app.config['SECRET_KEY'] = 'stephencurry30'
bootstrap = Bootstrap(app)
moment = Moment(app)


class NameForm(FlaskForm):
    name = StringField('你的名字？', validators=[DataRequired()])
    name_v = StringField('请再次输入', validators=[DataRequired()])
    submit = SubmitField('提交')


@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        if form.name.data != form.name_v.data:
            flash('两次输入的结果不一样，请重新输入')
        session['name'] = form.name.data
        return redirect(url_for('index'))
    return render_template('index.html', current_time=datetime.utcnow(), form=form,
                           name=session.get('name'))


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
