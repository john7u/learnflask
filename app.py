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
from flask_script import Shell, Manager
from flask_migrate import Migrate, MigrateCommand
from flask_mail import Mail, Message
from threading import Thread
basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['CSRF_ENABLED'] = True
app.config['SECRET_KEY'] = 'stephencurry30'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:abuseyoudna87@127.0.0.1:3306/learnflask?charset=utf8mb4'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True      # 该配置为True,则每次请求结束都会自动commit数据库的变动
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True     # 如果设置成 True (默认情况)，Flask-SQLAlchemy 将会追踪对象的修改
# 并且发送信号。这需要额外的内存， 如果不必要的可以禁用它。
app.config['MAIL_SERVER'] = 'smtp.126.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['FLASKY_ADMIN'] = os.environ.get('FLASKY_ADMIN')
app.config['FLASKY_MAIL_SUBJECT_PREFIX'] = '[FLASKY]'
app.config['FLASKY_MAIL_SENDER'] = 'Flasky Admin'
bootstrap = Bootstrap(app)
moment = Moment(app)
db = SQLAlchemy(app)
manager = Manager(app)
migrate = Migrate(app, db)
mail = Mail(app)


class NameForm(FlaskForm):
    name = StringField('你的名字？', validators=[DataRequired()])
    name_v = StringField('请再次输入', validators=[DataRequired()])
    submit = SubmitField('提交')


@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        if form.name.data == form.name_v.data:
            user = User.query.filter_by(username=form.name.data).first()
            if user is None:
                user = User(username=form.name.data)
                db.session.add(user)
                session['known'] = False
#                if app.config['FLASKY_ADMIN']:
#                   send_email(app.config['FLASKY_ADMIN'], 'You have a New User', 'mail/new_user', user=user)
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


class EmailHandler(Thread):
    def __init__(self, a, msg):
        super(EmailHandler, self).__init__()
        self.app = a
        self.msg = msg

    def send_sync_email(self):
        with self.app.app_context:
            mail.send(self.msg)


def send_email(to, subject, template, **kwargs):
    msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + subject,
                  sender=app.config['FLASKY_MAIL_SENDER'], recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    EmailHandler(app, msg).start()


def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role)


manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
    # app.run(debug=True)
