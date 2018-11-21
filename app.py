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
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:abuseyoudna87@127.0.0.1:3306/learnflask?charset=utf8mb4'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True      # 该配置为True,则每次请求结束都会自动commit数据库的变动
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True     # 如果设置成 True (默认情况)，Flask-SQLAlchemy 将会追踪对象的修改
# 并且发送信号。这需要额外的内存， 如果不必要的可以禁用它。
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
        user = User.query.filter_by(username=form.name.data).first()
        if form.name.data == form.name_v.data:
            if user is None:
                user = User(username=form.name.data)
                db.session.add(user)
                session['known'] = False
            else:
                session['known'] = True
            flash(u'欢迎回来,{}'.format(form.name.data), 'success')
            session['name'] = form.name.data
        else:
            flash(u'输入的名字不一致', 'danger')
            session['name'] = '陌生人'
        form.name.data = ''
        form.name_v.data = ''
        return redirect(url_for('index'))
    return render_template('index.html', current_time=datetime.utcnow(), form=form, name=session.get('name'),
                           known=session.get('known', False))


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


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role')  # backref向User模型中添加一个role属性

    def __repr__(self):
        return '<Role %r>' % self.name


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User %r>' % self.username  # print类实例将打印用户名


if __name__ == '__main__':
    app.run(debug=True)
