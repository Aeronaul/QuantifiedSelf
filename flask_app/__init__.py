from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///flask_app/data.db"
app.config['SECRET_KEY'] = '9b5cbe8a2867f99e06f0db3b'

db = SQLAlchemy()
db.init_app(app)
app.app_context().push()


Base = declarative_base()
engine = create_engine("sqlite:///flask_app/data.db")
Base.metadata.create_all(bind=engine)

from flask_app import routes
from flask_app.models import get_last_modified

app.jinja_env.globals.update(get_last_modified=get_last_modified)
