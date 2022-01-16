from flask import render_template, jsonify
from flask.views import MethodView
from models import Post, PostSchema
import json

class IndexView(MethodView):
    """
    On init, is rendered with Jinja, on update get data from Api using
    JavaScript and SocketIO.
    """

    def get(self):
        return render_template('index.html')


class PostView(MethodView):
    """Returns post data by id."""

    def get(self, post_id: int = None) -> dict:
        post_schema = PostSchema()
        posts_schema = PostSchema(many=True)

        if post_id:
            post = Post.query.filter_by(id=post_id).first()
            if post:
                return post_schema.dump(post)
            return {'message': 'Post does not exists.'}

        posts = Post.query.all()
        return {'posts': posts_schema.dumps(posts)}


class TestView(MethodView):
    """This is a View for testing the database."""

    def get(self):
        posts = Post.query.all()
        return posts.dump()
