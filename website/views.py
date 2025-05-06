#import external libraries
from flask import Blueprint, render_template

#set views blueprint
views=Blueprint("views", __name__)

#Home route
@views.route("/")
#home route function
def home():
    #returns homepage
    return render_template("home.html")
