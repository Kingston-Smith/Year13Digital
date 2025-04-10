#imports
from flask import Blueprint, render_template
#defining auth, this is used in __init__.py
auth=Blueprint("auth", __name__)
#routes, basically the code that tells it what the pages are, this section is for pages where users do stuff with their accounts
@auth.route("/sign-up")
@auth.route("/login")
@auth.route("/account")
def sign_up():
    return render_template("sign_up.html")
def login():
    return render_template("login.html")
def account():
    return render_template("account.html")