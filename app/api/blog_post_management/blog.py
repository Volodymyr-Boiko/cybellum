from flask import Blueprint, jsonify, request, session

from app.core.blog import (
    BlogPostDataCreate,
    core_create_post,
    core_get_post,
    core_get_posts,
)

blog_post_management = Blueprint("blog_post_management", __name__)


@blog_post_management.route("/create_post", methods=["POST"])
def create_post():
    data = request.form.to_dict()

    title = data.get("title")
    content = data.get("content")
    author_id = session.get("user_id")

    if not author_id:
        return jsonify({"error": "Login required"}), 401

    return core_create_post(
        BlogPostDataCreate(
            title=title,
            content=content,
            author_id=author_id,
        )
    )


@blog_post_management.route("/posts", methods=["GET"])
def get_all_posts():
    author_id = session.get("user_id")

    if not author_id:
        return jsonify({"error": "Login required"}), 401
    return core_get_posts()


@blog_post_management.route("/posts/<int:post_id>", methods=["GET"])
def get_post(post_id: int):
    author_id = session.get("user_id")

    if not author_id:
        return jsonify({"error": "Login required"}), 401

    return core_get_post(post_id)
