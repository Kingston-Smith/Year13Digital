#import external libraries
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
#import database
from . import db
#import the database models
from .models import User, Post

#set views blueprint
views=Blueprint("views", __name__)

#Home route
@views.route("/")
#home route function
def home():
    #returns homepage
    return render_template("home.html", user=current_user)

#Forum route
@views.route("/forum", methods=['GET', 'POST'])
@login_required
def forum():
    if request.method=="POST":
        title=request.form.get('title')
        content=request.form.get('content')
        if not title:
            flash('Your post needs a title', category='error')
        elif not content:
            flash('You need to put some content', category='error')
        else:
            post=Post(title=title, content=content, author=current_user.id)
            db.session.add(post)
            db.session.commit()
            flash('Post added!', category='success')
    return render_template("forum.html", user=current_user)

@views.route("/blog")
@login_required
def blog():
    posts=Post.query.all()
    return render_template("blog.html", user=current_user, posts=posts)