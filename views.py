from flask import render_template, jsonify, request
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
            One or more dictionaries with he public values of the Post model.
        """
        post_schema = PostSchema()
        posts_schema = PostSchema(many=True)

        if post_id:
            post = Post.query.get_or_404(post_id)
            return post_schema.dump(post)

        title = request.args.get('title')

        if title:
            posts = Post.query.filter(Post.title.match(title)).order_by(Post.datetime.desc()).limit(50).all()
        else:
            posts = Post.query.order_by(Post.datetime.desc()).limit(50).all()

        return jsonify(_total=len(posts_schema.dump(posts)), posts=posts_schema.dump(posts))
