from datetime import datetime as dt
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields


db = SQLAlchemy()


class Newsletter(db.Model):
    __tablename__ = 'newsletters'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False, index=True, unique=True)

    def __str__(self):
        return self.name


class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False, index=True, unique=True)

    def __str__(self):
        return self.name


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256), nullable=False, index=True)
    description = db.Column(db.String(512), nullable=True, index=True)
    author = db.Column(db.String(128), nullable=True, index=True)
    url = db.Column(db.String(512), nullable=True, index=True)
    datetime = db.Column(db.DateTime, default=dt.utcnow, index=True)

    newsletter_id = db.Column(db.Integer, db.ForeignKey('newsletters.id', ondelete='CASCADE'))
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))

    def __str__(self):
        return self.title


class PostSchema(Schema):
    title = fields.Str()
    description = fields.Str()
    author = fields.Str()
    datetime = fields.Date()
