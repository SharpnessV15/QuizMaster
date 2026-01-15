from flask import Flask,render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
app = Flask(__name__)
app.config['SECRET_KEY']= 'e60b224224c50fb846f1b04b'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quiz.db'
db=SQLAlchemy(app)
login_manager=LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'danger'