from flask import Flask, jsonify
from flask_restful import Api, Resource, reqparse

import db_actions
from db import create_db


app = Flask(__name__)
api = Api(app)


class Post(Resource):
    def get(self, id=0):
        if not id:
            posts = db_actions.get_posts()
            return row_to_json(posts)

        post = db_actions.get_post(id)
        if post:
            return row_to_json([post])

        return "Відсутні статті"

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("author")
        parser.add_argument("text")
        params = parser.parse_args()
        id = db_actions.add_post(**params)
        answer = jsonify(f"Статтю успішно додано під id {id}")
        answer.status_code = 200
        return answer

    def put(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument("author")
        parser.add_argument("text")
        params = parser.parse_args()
        answer = db_actions.update_post(id, **params)
        answer = jsonify(answer)
        answer.status_code = 200
        return answer

    def delete(self, id):
        answer = jsonify(db_actions.delete_post(id))
        answer.status_code = 200
        return answer


def row_to_json(posts: list):
    posts_json = []

    for post in posts:
        posts_json.append({
            "id": post.id,
            "author": post.author,
            "text": post.text
        })

    posts_json = jsonify(posts_json)
    posts_json.status_code = 200

    return posts_json


api.add_resource(Post, "/api/posts/", "/api/posts/<int:id>/")


if __name__ == "__main__":
    create_db()
    app.run(debug=True, port=3000)