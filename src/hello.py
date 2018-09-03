'''
Created on 2018年4月11日

@author: g
'''

from flask import Flask, request, render_template, redirect, session, url_for, flash
from flask_bootstrap import Bootstrap
from flask_mail import Mail, Message
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from sqlalchemy.orm import backref
from flask_script import Manager

from config import config


app = Flask(__name__)
app.config.from_object(config['development'])
db = SQLAlchemy(app)
bootstrap = Bootstrap(app)
moment = Moment(app)
mail = Mail(app)
manager = Manager(app)

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role')

    def __repr__(self):
        return '<Role %r>' % self.name

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(255), unique=True, index=True)
    password = db.Column(db.String(255))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    posts = db.relationship('Post', backref='user', lazy='dynamic')
    
    def __repr__(self):
        return '<User %r>' % self.username

tags = db.Table('post_tags',
                db.Column('post_id', db.Integer(), db.ForeignKey('posts.id')),
                db.Column('tag_id', db.Integer(), db.ForeignKey('tags.id')))

class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(255))
    text = db.Column(db.Text())
    publish_date = db.Column(db.DateTime())
    comments = db.relationship('Comment', backref='post', lazy='dynamic')
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'))
    tags = db.relationship('Tag', secondary=tags, backref=db.backref('posts', lazy='dynamic'))

    def __init__(self, title):
        self.title = title

    def __repr__(self):
        return "<Post '{}'>".format(self.title)

class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(255))
    text = db.Column(db.Text())
    date = db.Column(db.DateTime())
    post_id = db.Column(db.Integer(), db.ForeignKey('posts.id'))

    def __repr__(self):
        return "<Comment '{}'>".format(self.text[:15])

class Tag(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(255))
    
    def __init__(self, title):
        self.title = title
        
    def __repr__(self):
        return "<Tag '{}'>".format(self.title)

def send_mail(to, subject, template, **kwargs):
    msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + subject,
                  sender=app.config['FLASKY_MAIL_SENDER'],
                  recipients=[to]
                  )
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    mail.send(msg)

if __name__ == '__main__':
    manager.run()
