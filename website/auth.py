#import external libraries
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

#import database
from . import db

#import from .models user
from .models import User

#Setting auth blueprint
auth=Blueprint("auth", __name__)

#routes

#sign up
@auth.route("/sign-up", methods=['GET', 'POST'])
def sign_up():
    if request.method=='POST':
        email=request.form.get("email")
        username=request.form.get("username")
        password1=request.form.get("password1")
        password2=request.form.get("password2")

        email_exists=User.query.filter_by(email=email).first()
        username_exists=User.query.filter_by(username=username).first()

        if email_exists:
            flash('email is taken', category='error')
        elif username_exists:
            flash('username is taken', category='error')
        elif password1!=password2:
            flash('Confirmation password does not match', category='error')
        elif len(password1)<8:
            flash('password must be at least 8 characters', category='error')
        elif len(password1)>20:
            flash('password can not be more than 20 characters', category='error')
        elif len(username)<2:
            flash('username must be at least 2 characters', category='error')
        elif len(email)<4:
            flash('Email is invalid', category='error')
        else:
            new_user=User(email=email, username=username, password=generate_password_hash(password1, method='scrypt:32768:8:1'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('your account has been created!', category='success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html")
    
#log in    
@auth.route("/login")
def login():
    return render_template("login.html")

#account
@auth.route("/account")
def account():
    return render_template("account.html")
