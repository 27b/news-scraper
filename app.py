from flask import Flask
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from multiprocessing import Process
from crawler.crawler import Crawler
from models import db, Newsletter, Category
from sqlalchemy import create_engine, inspect
from views import BlobView, IndexView, PostView
from dotenv import load_dotenv
from os import getenv

#
# Flask configuration
#

load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = getenv('DB_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = eval(getenv('DB_MODIFICATIONS'))
app.config['DEBUG'] = eval(getenv('DEBUG_MODE'))
db.init_app(app)
migrate = Migrate(app=app, db=db)
ma = Marshmallow(app)

#
# Flask endpoints
#

app.add_url_rule('/', view_func=IndexView.as_view('index'))
app.add_url_rule('/api/post/', view_func=PostView.as_view('posts'))
app.add_url_rule('/api/post/<int:post_id>', view_func=PostView.as_view('post'))
app.add_url_rule('/api/blob/', view_func=BlobView.as_view('blobs'))

daemon = Process(target=Crawler.run_task, args=(app, db))


if __name__ == '__main__':
    engine = create_engine(getenv('DB_URI'))
    
    newsletters = ['NYTimes', 'Time', 'WashingtonPost']
    categories = ['business', 'politics', 'technology', 'science', 'world', \
                  'books', 'style', 'education', 'health', 'sports', 'arts', \
                  'television', 'climate', 'automobile']

    with app.app_context():
        # if there are no tables in the database do:
        if not inspect(engine).has_table('newsletters'):
            db.create_all()
        
            for name in newsletters:
                newsletter = Newsletter(name=name)
                db.session.add(newsletter)

            for name in categories:
                category = Category(name=name)
                db.session.add(category)
        
            db.session.commit()
    
        # If there are new categories/newsletters do:
        newsletters_db = [N.name for N in Newsletter.query.all()]
        categories_db = [C.name for C in Category.query.all()]
    
        for n in list(filter(lambda n: n not in newsletters_db, newsletters)):
            print('Adding newsletter:', n)
            newsletter = Newsletter(name=n)
            db.session.add(newsletter)
            db.session.commit()

        for c in list(filter(lambda c: c not in categories_db, categories)):
            print('Adding category:', c)
            category = Category(name=c)
            db.session.add(category)
            db.session.commit()
    
    daemon.start()
    # daemon.join()  # Remove the hash for view the logs (the app will not run)

    app.run()
