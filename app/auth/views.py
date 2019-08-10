from . import auth
from flask import render_template, flash, request, redirect, url_for
from flask_login import login_user,logout_user,login_required
from .forms import LoginForm
from ..models import User
from .forms import PasswordResetForm,RegisterForm,ChangeEmailForm,ChangePasswordForm,PasswordReserRequestForm
from app import db
from ..email import send_mail
from flask_login import current_user

@auth.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash("Invalid username or password")
    return render_template('auth/login.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out')
    return redirect(url_for('main.index'))

@auth.route('/register',methods=['GET','POST'])
def register():
    form=RegisterForm()
    if form.validate_on_submit():
        user=User(email=form.email.data,username=form.username.data,password=form.password.data)
        db.session.add(user)
        db.session.commit()
        token=user.generate_confirmation_token()
        send_mail(user.email,'Confirm your Account','auth/email/confirm',user=user,token=token)
        flash("A confirmation has been sent to your email")
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html',form=form)

@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        flash('Your have confirmed your account.Thanks')
    else:
        flash("The confirmation link is invalid or has expired")
    return redirect(url_for('main.index'))

@auth.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.ping()
        if not current_user.confirmed and request.endpoint[0:5]!="auth.":
            return redirect(url_for('auth.unconfirmed'))

@auth.route('/unconfirm')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')

@auth.route('/confirm')
@login_required
def resend_email():
    token=current_user.generate_confirmation_token()
    send_mail(current_user.email,"Confirm your Account",'auth/email/confirm',user=current_user,token=token)
    flash('A new confirmation email has been sent to you by email')
    return redirect(url_for('main.index'))
    

@auth.route('/change-password',methods=['GET','POST'])
@login_required
def change_password():
    form=ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.password=form.password.data
            db.session.add(current_user)
            db.session.commit()
            flash("Your password has been updated")
            return redirect(url_for('main.index'))
        else:
            flash("Invalid password")
    return render_template("auth/change_password.html",form=form)

@auth.route('/reset',methods=['GET','POST'])
def password_reset_request():
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form=PasswordReserRequestForm()
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        if user:
            token=user.generate_reset_token()
            send_mail(user.email,'Reset your password','auth/email/reset_password',user=user,token=token)
        flash("An email with instructions to reset your password has been sent to you")
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html',form=form)

@auth.route('/reset/<token>',methods=['GET','POST'])
def password_reset(token):
    if not current_user.i_sanonymous:
        return redirect(url_for('main.index'))
    form=PasswordResetForm()
    if form.validate_on_submit():
        if User.reset_password(token,form.password.data):
            db.session.commit()
            flash('Your password has been updated')
            return redirect(url_for('auth.login'))
        else:
            return redirect(url_for('main.index'))
    return render_template('auth/reset_password.html',form=form)

@auth.route('/change_email',methods=['GET','POST'])
@login_required
def change_email_request():
    form=ChangeEmailForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.password.data):
            new_email=form.email.data
            token=current_user.generate_change_email_token(new_email)
            send_mail(new_email,'Confirm your email address','auth/email/change_email',user=current_user,token=token)
            flash("An email with instructions to confirm your new email address has been sent to you")
            return redirect(url_for('main.index'))
        else:
            flash('Invalid email or password')
    return render_template('auth/change_email.html',form=form)

@auth.route('/change_email/<token>')
@login_required
def change_email(token):
    if current_user.change_email(token):
        db.session.commit()
        flash("Your email has been updated")
    else:
        flash('Invalid request')
    return redirect(url_for('main.index'))
