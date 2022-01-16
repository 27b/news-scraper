from flask import Flask
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from multiprocessing import Process
from crawler.crawler import Crawler
from models import db, Newsletter, Category, Post
from views import IndexView, PostView, TestView
from dotenv import load_dotenv
from os import getenv


# Flask configuration
load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = getenv('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = eval(getenv('TRACK_MODIFICATIONS'))
app.config['DEBUG'] = eval(getenv('DEBUG_MODE'))
db.init_app(app)
migrate = Migrate(app=app, db=db)
ma = Marshmallow(app)


# Flask urls
app.add_url_rule('/', view_func=IndexView.as_view('index'))
app.add_url_rule('/post/', view_func=PostView.as_view('posts'))
app.add_url_rule('/post/<int:post_id>', view_func=PostView.as_view('post'))
app.add_url_rule('/test/', view_func=TestView.as_view('tests'))


daemon = Process(target=Crawler.run_task, args=(db,))


if __name__ == '__main__':
    with app.app_context():
        # db.drop_all()
        db.create_all()
        n1 = Newsletter(name='NYTimes')
        c1 = Category(name='economy')
        db.session.add(n1)
        db.session.add(c1)
        db.session.commit()

        daemon.start()

    app.run()
