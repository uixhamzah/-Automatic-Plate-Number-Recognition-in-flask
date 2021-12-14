from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail, Message
import os
# from flask_migrate import Migrate


# Init run
app = Flask(__name__)
basedir = os.path.dirname(os.path.dirname(__file__))
mail=Mail(app)


# konfigurasi database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' +os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site2.db'
app.config['SQLALCHEMY_BINDS'] = {
   # 'db2': 'sqlite:////home/aryan2019/Desktop/Flask/ANPR_Chroma/flaskblog/site2.db'
   'db2': 'sqlite:///C:/projectsPython/ANPR-Chroma-main/ANPR_Chroma/flaskblog/database.db'
}

# initialize database
db = SQLAlchemy(app)
ma = Marshmallow(app)

# db.create_all()
# migrate = Migrate(app, db)

app.config['MAIL_SERVER'] = 'localhost'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] ='yourgmail@gmail.com'
app.config['MAIL_PASSWORD'] = 'your password'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail=Mail(app)

bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from flaskblog import routes
