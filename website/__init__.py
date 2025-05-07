#importing external libraries
from flask import Flask

#this creates the app
def create_app():
    #returns app
    app=Flask(__name__)
    
#Importing views and auth from views.py and auth.py and registering blueprints
    from .views import views

    app.register_blueprint(views, url_prefix="/")

    from .auth import auth

    app.register_blueprint(auth, url_prefix="/")

    return app
