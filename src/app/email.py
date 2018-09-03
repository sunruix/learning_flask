'''
Created on 2018年4月28日

@author: sunrui
'''
from threading import Thread
from flask import (current_app, render_template)
from flask_mail import Message
from jinja2.exceptions import TemplateNotFound

from . import main, mail

def send_msg(current_context, msg):
    with current_context:
        mail.send(msg)

def send_async_mail(msg):
    thr = Thread(target=send_msg, args=[current_app.app_context(), msg])
    thr.start()

def send_mail(to, subject, template, **kwargs):
    msg = Message(current_app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + subject,
                  sender=current_app.config['FLASKY_MAIL_SENDER'],
                  recipients=[to]
                  )
    try:
        msg.body = render_template(template + '.txt', **kwargs)
        msg.html = render_template(template + '.html', **kwargs)
    except TemplateNotFound:
        pass
    send_async_mail(msg)
#     mail.send(msg)