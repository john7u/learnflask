#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, make_response, render_template, session, url_for, redirect, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
import pymysql
import os
basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['CSRF_ENABLED'] = True
app.config['SECRET_KEY'] = 'stephencurry30'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://' + 'root:abuseyoudna@127.0.0.1/' \
                                        + os.path.join(basedir, 'db.learnflask')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
bootstrap = Bootstrap(app)
moment = Moment(app)
db = SQLAlchemy(app)


class NameForm(FlaskForm):
    name = StringField('你的名字？', validators=[DataRequired()])
    name_v = StringField('请再次输入', validators=[DataRequired()])
    submit = SubmitField('提交')


@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        if form.name.data == form.name_v.data:
            flash(u'欢迎回来,{}'.format(form.name.data), 'success')
            session['name'] = form.name.data
        else:
            flash(u'输入的名字不一致', 'danger')
            session['name'] = '陌生人'
        return redirect(url_for('index'))
    return render_template('index.html', current_time=datetime.utcnow(), form=form, name=session.get('name'))


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
