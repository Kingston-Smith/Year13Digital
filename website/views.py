#imports
from flask import Blueprint, render_template
#defining views (used in __init__)
views=Blueprint("views", __name__)
#routes, this is where pages that don't heavily deal with the users account go
@views.route("/")
@views.route("/home")
def home():
    return render_template("home.html")