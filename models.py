from datetime import datetime as dt
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields
from sqlalchemy import desc

db = SQLAlchemy()


class Newsletter(db.Model):
    '''Newsletter model

    Args:
        name: max 32 chars.
    '''
    __tablename__ = 'newsletters'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False, index=True, unique=True)

    def __str__(self):
        return self.name


class Category(db.Model):
    '''Category model
    
    Args:
        name: max 32 chars.
    '''
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False, index=True, unique=True)

    def __str__(self):
        return self.name


class Post(db.Model):
    '''Category model.
    
    Args:
        title: 256 chars.
        description: 512 chars.
        author: 128 chars.
        url: 512 chars.
    '''
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256), nullable=False, index=True)
    description = db.Column(db.String(512), nullable=True, index=True)
    author = db.Column(db.String(128), nullable=True, index=True)
    url = db.Column(db.String(512), nullable=True, index=True)
    datetime = db.Column(db.DateTime, default=dt.utcnow, index=True)

    newsletter_id = db.Column(db.Integer, db.ForeignKey('newsletters.id', ondelete='CASCADE'))
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))

    def is_valid(self) -> tuple[bool, str]:
        '''Check if the post is valid by checking the length of the
        title, description and author, also check if the post is
        already in the database using the title and description.
        
        Returns:
            tuple: first value is the status (bool) and the second \
                   value is the message.
        '''
        title = self.title
        description = self.description
        author = self.author

        if len(title) > 256: return (False, 'Title invalid.')
        if len(description) > 512: return (False, 'Description invalid.')
        if len(author) > 128: return (False, 'Author invalid.')

        if self.query.filter_by(title=title, description=description).first():
            return (False, 'Post alredy in database.')
        
        return (True, 'Post valid.')

    def __str__(self):
        return self.title


class PostSchema(Schema):
    '''Post Schema, used to serialize post type objects using the
    marshmallow library.'''
    id = fields.Str()
    title = fields.Str()
    description = fields.Str()
    author = fields.Str()
    datetime = fields.Str()
    newsletter_id = fields.Str()
    category_id = fields.Str()
    url = fields.Str()
    
    class Meta:
        ordered = True