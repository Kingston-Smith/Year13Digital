#import external libraries
from flask import Blueprint, render_template

#Setting auth blueprint
auth=Blueprint("auth", __name__)

#routes

#sign up
@auth.route("/sign-up")
def sign_up():
    return render_template("sign_up.html")
    
#log in    
@auth.route("/login")
def login():
    return render_template("login.html")

#account
@auth.route("/account")
def account():
    return render_template("account.html")
