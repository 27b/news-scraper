from flask import render_template, jsonify
from flask.views import MethodView


class IndexView(MethodView):
    """
    On init, is rendered with Jinja, on update get data from Api using
    JavaScript and SocketIO.
    """

    def get(self):
        return render_template('index.html')


class PostView(MethodView):
    """Returns post data by id."""

    def get(self, post_id: int):
        return {'id': post_id}
