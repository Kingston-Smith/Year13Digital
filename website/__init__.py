#importing external libraries
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db=SQLAlchemy()
DB_NAME="database.db"

#this creates the app
def create_app():
    #returns app
    app=Flask(__name__)
    app.config['SECRET_KEY']="388ud40ii03do43lpdekwfckojehwuftdeeduiqowpdslpodojsijdoipowpkdiojpewiifhr8498323ijoidj8edc98eis4w134w152t3tupw3popoi90wdpoewidouhouiudhe"
    app.config['SQLALCHEMY_DATABASE_URI']=f'sqlite:///{DB_NAME}'
    db.init_app(app)
    
    #Importing views and auth from views.py and auth.py and the user database from models and registering blueprints
    from .views import views
    app.register_blueprint(views, url_prefix="/")
    from .auth import auth
    app.register_blueprint(auth, url_prefix="/")
    from .models import User
    
    #If database doesn't exist create it, won't do much after the first usage
    #but dont delete it in case you decide to update what information databases store
    with app.app_context():
        db.create_all()

    #login manager stuff    
    login_manager=LoginManager()
    login_manager.login_view="auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app
