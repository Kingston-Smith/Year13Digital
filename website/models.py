from . import db
from sqlalchemy.sql import func
from flask_login import UserMixin

#This doesn't store the information, but it's used in the database creation.

#User database model
class User(db.Model, UserMixin):
    id=db.Column(db.Integer, primary_key=True)
    email=db.Column(db.String(150), unique=True)
    username=db.Column(db.String(150), unique=True)
    password=db.Column(db.String(20))
    date_created=db.Column(db.String)
    posts=db.Relationship('Post', backref="user", passive_deletes=True)
    comments=db.Relationship('Comment', backref='user', passive_deletes=True)
    likes=db.Relationship('Like', backref='user', passive_deletes=True)


#Posts database model
class Post(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(100), nullable=False)
    content=db.Column(db.Text, nullable=False)
    date_created=db.Column(db.String)
    last_updated=db.Column(db.String)
    author=db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    comments=db.Relationship('Comment', backref='post', passive_deletes=True)
    likes=db.Relationship('Like', backref='post', passive_deletes=True)

#Comments database model
class Comment(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    text=db.Column(db.String(150), nullable=False)
    date_created=db.Column(db.String)
    last_updated=db.Column(db.String)
    author=db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    post_id=db.Column(db.Integer, db.ForeignKey('post.id', ondelete="CASCADE"), nullable=False)

#likes database model
class Like(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    date_created=db.Column(db.String)
    author=db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    post_id=db.Column(db.Integer, db.ForeignKey('post.id', ondelete="CASCADE"), nullable=False)