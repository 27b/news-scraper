from flask import render_template
from flask.views import MethodView
from models import Post, PostSchema


class IndexView(MethodView):
    """
    On init, is rendered with Jinja, on update get data from Api using
    JavaScript and SocketIO.
    """

    def get(self):
        """
        Return a page, and coming soon use Jinja for render the view with the
        last posts.
        """
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
