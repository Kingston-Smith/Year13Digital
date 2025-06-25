#import external libraries
from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_user, logout_user, login_required, current_user
#import database
from . import db
#import the database models
from .models import User, Post, Comment, Like
#importing from .forms
from .forms import PostForm, CommentForm
#Importing the time
from datetime import datetime


#set views blueprint
views=Blueprint("views", __name__)

#Home route
@views.route("/")
#home route function
def home():
    #returns homepage
    return render_template("home.html", user=current_user)

#Create post route
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
            return redirect(url_for('views.blog'))
    return render_template("forum.html", user=current_user)

#update post route
@views.route("/update-post/<id>", methods=['GET', 'POST'])
@login_required
def update_post(id):
    post=Post.query.filter_by(id=id).first()
    form=PostForm()
    if not post:
        flash("post does not exist, i'm not exactly sure how you managed to do this", category="error")
    elif current_user.id!=post.author:
        flash("You can't update someone elses post", category="error")
    elif form.validate_on_submit():
        if post.title!=form.title.data or post.content!=form.content.data:
            post.title=form.title.data
            post.content=form.content.data
            post.last_updated=datetime.now()
            db.session.commit()
            flash('Post updated successfully', category='success')
        else:
            flash('You did not actually change anything', category="success")
        page=request.args.get('page', 1, type=int)
        posts=Post.query.order_by(Post.date_created.desc()).paginate(page=page, per_page=4)
        return render_template("blog.html", user=current_user, posts=posts)
    elif request.method=='GET':
        form.title.data=post.title
        form.content.data=post.content
    return render_template("update_posts.html", form=form, user=current_user, posts=post)

#update comment route
@views.route("/update-comment/<id>", methods=['GET', 'POST'])
@login_required
def update_comment(id):
    comment=Comment.query.filter_by(id=id).first()
    form=CommentForm()
    if not comment:
        flash("comment does not exist", category="error")
    elif current_user.id!=comment.author:
        flash("You can't update someone elses comment", category="error")
    elif form.validate_on_submit():
        if comment.text!=form.content.data:
            comment.text=form.content.data
            comment.last_updated=datetime.now()
            db.session.commit()
            flash('Comment updated successfully', category='success')
        else:
            flash('You did not actually change anything', category='success')
        page=request.args.get('page', 1, type=int)
        posts=Post.query.order_by(Post.date_created.desc()).paginate(page=page, per_page=4)
        return render_template("blog.html", user=current_user, posts=posts)
    elif request.method=='GET':
        form.content.data=comment.text
    return render_template("update_comments.html", form=form, user=current_user, comments=comment)

@views.route("/blog")
@login_required
def blog():
    page=request.args.get('page', 1, type=int)
    posts=Post.query.order_by(Post.date_created.desc()).paginate(page=page, per_page=4)
    return render_template("blog.html", user=current_user, posts=posts)

#delete post route
@views.route("/delete-post/<id>", methods=['GET', 'POST'])
@login_required
def delete_post(id):
    post=Post.query.filter_by(id=id).first()
    if not post:
        flash("post does not exist, i'm not exactly sure how you managed to do this", category="error")
    elif current_user.id!=post.author:
        flash("You can't delete someone elses post", category="error")
    else:
        for comment in post.comments:
            db.session.delete(comment)
        for like in post.likes:
            db.session.delete(like)
        db.session.delete(post)
        db.session.commit()
        flash('Post deleted!', category='success')
    return redirect(url_for('views.blog'))

@views.route("/create-comment/<post_id>", methods=['POST'])
@login_required
def create_comment(post_id):
    text=request.form.get('text')
    if not text:
        flash("Comment can not be empty", category="error")
    else:
        post=Post.query.filter_by(id=post_id)
        if post:
            comment=Comment(text=text, author=current_user.id, post_id=post_id)
            db.session.add(comment)
            db.session.commit()
            flash('Comment added', category='success')
        else:
            flash('The post you are trying to comment on does not exist', category='error')
    return redirect(url_for('views.blog'))

#Delete comment
@views.route("/delete-comment/<comment_id>", methods=['GET', 'POST'])
@login_required
def delete_comment(comment_id):
    comment=Comment.query.filter_by(id=comment_id).first()
    if not comment:
        flash("comment does not exist, i'm not exactly sure how you managed to do this", category="error")
    elif current_user.id!=comment.author and current_user.id!=comment.post.author:
        flash("You must either own the post or the comment to delete a comment", category="error")
    else:
        db.session.delete(comment)
        db.session.commit()
        flash('Comment deleted!', category='success')
    return redirect(url_for('views.blog'))

#like route
@views.route("/like-post/<post_id>", methods=['POST'])
@login_required
def like(post_id):
    post=Post.query.filter_by(id=post_id).first()
    like=Like.query.filter_by(author=current_user.id, post_id=post_id).first()

    if not post:
        return jsonify({'error':'post does not exist'}, 400)
    elif like:
        db.session.delete(like)
        db.session.commit()
    else:
        like=Like(author=current_user.id, post_id=post_id)
        db.session.add(like)
        db.session.commit()
    return jsonify({'likes': len(post.likes), "liked": current_user.id in map(lambda x: x.author, post.likes)})