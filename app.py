from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from views import (IndexView, PostView)
from os import getenv
from dotenv import load_dotenv

# Flask configuration
app = Flask(__name__)
app.config['SECRET_KEY'] = getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = getenv('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = getenv('TRACK_MODIFICATIONS')
app.config['DEBUG'] = getenv('DEBUG_MODE')

db = SQLAlchemy(app=app)
migrate = Migrate(app=app, db=db)


# Flask urls
app.add_url_rule('/', view_func=IndexView.as_view('index'))


if __name__ == '__main__':
    app.run()
