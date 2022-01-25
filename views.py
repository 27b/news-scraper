from flask import render_template
from flask.views import MethodView
from models import Post, PostSchema


class IndexView(MethodView):
    """On init, is rendered with Jinja, on update get data from Api using
    JavaScript and SocketIO.
    """

    @staticmethod
    def get():
        """Send the static page with the database posts rendered by Jinja.

        Returns:
            Jinja template
        """
        return render_template('index.html')


class PostView(MethodView):
    """Returns post data by id."""

    @staticmethod
    def get(post_id: int = None) -> dict:
        """If not post_id return a list of posts.

        Args:
            post_id: An integer to search in the database.

        Returns:
            One or more dictionaries with the public values of the Post model.
        """
        post_schema = PostSchema()
        posts_schema = PostSchema(many=True)

        if post_id:
            post = Post.query.get_or_404(post_id)
            return post_schema.dump(post)

        posts = Post.query.all()
        return {'posts': posts_schema.dumps(posts)}
