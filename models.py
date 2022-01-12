from app import db
from datetime import datetime as dt


class Newsletter(db.Model):
    __tablename__ = 'newsletters'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False)

    def __str__(self):
        return self.name


class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False, index=True)

    def __str__(self):
        return self.name


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False, index=True)
    description = db.Column(db.String(256), nullable=True, index=True)
    author = db.Column(db.String(64), nullable=True, index=True)
    content = db.Column(db.Text, nullable=True, index=True)
    datetime = db.Column(db.String(32))
    added_in = db.Column(db.DateTime, default=dt.utcnow, index=True)

    newsletter_id = db.Column(db.Integer, db.ForeignKey('newsletters.id', ondelete='CASCADE'))
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))

    def __str__(self):
        return self.title
