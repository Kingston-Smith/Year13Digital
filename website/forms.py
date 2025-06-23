#Importing from external libraries
from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, length, ValidationError
#Importing user database from models
from .models import User

#form for updating posts
class PostForm(FlaskForm):
    title=StringField('Title', validators=[DataRequired()])
    content=TextAreaField('Content', validators=[DataRequired()])
    submit=SubmitField('Update')

#form for updating comments
class CommentForm(FlaskForm):
    content=TextAreaField('Content', validators=[DataRequired()])
    submit=SubmitField('Update')