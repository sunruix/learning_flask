'''
Created on 2018年5月7日

@author: sunrui
'''
from flask import (render_template,
                   redirect,
                   request,
                   url_for,
                   flash)
from flask_login import (login_user,
                         logout_user,
                         current_user,
                         login_required)

from .. import db
from . import auth
from ..models import User
from .forms import (LoginForm,
                    RegistrationForm,
                    ChangePasswordForm,
                    ChangeEmailForm)
from ..email import send_mail

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('Invalid username or password.', 'error')
    return render_template('auth/login.html', form=form)

@auth.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        send_mail(user.email,
                   'Confirm your account in Flasky',
                   'auth/email/confirm',
                   user=user,
                   token=token)
        flash('You can now login')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)

@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        flash('You have confirmed your account. Thanks!', 'info')
    else:
        flash('The confirmation link is invalid or has expired.')
    return redirect(url_for('main.index'))

@auth.before_app_request
def before_request():
    print(request, ':', request.endpoint)
    if current_user.is_authenticated:
        current_user.ping()
        if not current_user.confirmed and request.endpoint[:5] != 'auth.':
            return redirect(url_for('auth.unconfirmed'))

@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')

@auth.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_mail(current_user.email,
              'Confirm Your Account',
              'auth/email/confirm',
              user=current_user, token=token)
    flash('A confirmation email has been sent to you by email.')
    return redirect(url_for('main.index'))

@auth.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.password = form.password.data
            db.session.add(current_user)
            flash('Your password has been updated.')
            return redirect(url_for('main.index'))
        else:
            flash('Invalid password.')
    return render_template('auth/change_password.html', form=form)

@auth.route('/change-email', methods=['GET', 'POST'])
@login_required
def change_email():
    form = ChangeEmailForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            new_email = form.email.data
            token = current_user.generate_email_change_token(new_email)
            send_mail(new_email,
                      'Confirm Your Email Address.',
                      'auth/email/change_email',
                      user=current_user, token=token)
            flash('A confirmation email has been sent to your new email address.')
            return redirect(url_for('main.index'))
        else:
            flash('Invalid password.')
    return render_template('auth/change_email.html', form=form)

@auth.route('/change-email/<token>')
@login_required
def change_email_confirmation(token):
    if current_user.change_email(token):
        flash('Your email address has been updated.')
    else:
        flash('The confirmation link is invalid or has expired.')
    return redirect(url_for('main.index'))
