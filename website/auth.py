# import external libraries
from datetime import datetime
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

# Some of the routes are in here, the others are in views. Put routes to do with user authentication here, and other routes in views

# import database
from . import db

# import users, posts, comments, and likes from models, the last two arent used here but I added for future convenience
from .models import User, Post, Comment, Like

# Setting auth blueprint
auth = Blueprint("auth", __name__)

# importing time

# routes

# sign up


@auth.route("/sign-up", methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        # Getting the information from the page
        email = request.form.get("email")
        username = request.form.get("username")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        # This basically tries to match the username and password to the database to check if they are taken.
        email_exists = User.query.filter_by(email=email).first()
        username_exists = User.query.filter_by(username=username).first()

        # This checks everything for issues
        if email_exists:
            flash('email is taken', category='error')
        elif username_exists:
            flash('username is taken', category='error')
        elif password1 != password2:
            flash('Confirmation password does not match', category='error')
        elif len(password1) < 8:
            flash('password must be at least 8 characters', category='error')
        elif len(password1) > 20:
            flash('password can not be more than 20 characters', category='error')
        elif len(username) < 2:
            flash('username must be at least 2 characters', category='error')
        elif len(username) > 20:
            flash('username must be at most 20 characters', category='error')
        elif len(email) < 4:
            flash('Email is invalid', category='error')
        else:
            # Creating the user
            new_user = User(email=email, username=username, password=generate_password_hash(
                password1, method='scrypt:32768:8:1'), date_created="{:%B %d, %Y %H:%M:%S}".format(datetime.now()))
            db.session.add(new_user)
            db.session.commit()
            # Logging in the user
            login_user(new_user, remember=True)
            flash('Your account has been created!', category='success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)

# log in


@auth.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get email and password from the form
        email = request.form.get("email")
        password = request.form.get("password")

        # Check the database for any users with the entered email address
        user = User.query.filter_by(email=email).first()
        # If the email exists in the database
        if user:
            # Checks if the existing user has the same password as entered
            if check_password_hash(user.password, password):
                # Logs in
                flash("Welcome back", category="success")
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            # tells user what they did wrong
            else:
                flash("Password does not match", category="error")
        else:
            flash("There is no account with this Email, to create a new account go to the account creation page", category="error")

    return render_template("login.html", user=current_user)

# account page


@auth.route("/account/<username>", methods=['GET', 'POST'])
@login_required
def account(username):
    if request.method == "POST":
        # This gets the username of the user that is being viewed
        username = request.form.get("username")
    # Stuff for seperating posts into pages
    page = request.args.get('page', 1, type=int)
    # Checking if the user exists
    user = User.query.filter_by(username=username).first()
    if not user:
        flash("User does not exist", category="error")
        return redirect(url_for('views.blog'))
    # Getting the posts
    posts = Post.query.filter_by(user=user).order_by(
        Post.date_created.desc()).paginate(page=page, per_page=4)
    return render_template("account.html", user=current_user, posts=posts, username=username)

# This logs users out


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('views.home'))

# This is what runs when an account is deleted, be careful with this code


@auth.route("/delete-account/<id>")
@login_required
def delete_account(id):
    # Gets the user
    user = User.query.filter_by(id=id).first()
    # Checks for user existence
    if not user:
        flash("The account you are trying to delete does not exist", category="error")
    # Checks if the logged in user is actually the account owner
    elif user.id != current_user.id:
        flash("You can't delete someone elses account", category="error")
    # This next part is where account deletion starts
    else:
        # Log the user out
        logout_user()
        # For every comment the user has made, delete it.
        for comment in user.comments:
            db.session.delete(comment)
        # This checks for every post the user has made, then it checks for every comment and like on those posts
        # It then deletes the comments, and the likes, and the posts
        for post in user.posts:
            for comment in post.comments:
                db.session.delete(comment)
            for like in post.likes:
                db.session.delete(like)
            db.session.delete(post)
        # This deletes all likes made by the user
        for like in user.likes:
            db.session.delete(like)
        # This deletes the user then commits
        db.session.delete(user)
        db.session.commit()
        flash("account deleted successfully", category="success")
    return redirect(url_for('views.home'))
