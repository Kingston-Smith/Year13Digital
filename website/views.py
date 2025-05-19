#import external libraries
from flask import Blueprint, render_template
from flask_login import login_user, logout_user, login_required, current_user

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
    return render_template("forum.html", user=current_user)