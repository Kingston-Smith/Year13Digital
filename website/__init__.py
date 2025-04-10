#importing the class Flask from flask
from flask import Flask
#this creates the app, just don't touch this
def create_app():
    app=Flask(__name__)
#Importing views and auth and rendering (see views.py and auth.py)
    from .views import views

    app.register_blueprint(views, url_prefix="/")

    from .auth import auth

    app.register_blueprint(auth, url_prefix="/")

    return app