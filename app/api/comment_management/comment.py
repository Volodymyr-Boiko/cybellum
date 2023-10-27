from flask import Blueprint, jsonify, request, session

from app.core.comment import CommentDataCreate, core_create_comment, core_get_comments

comment_management = Blueprint("comment_management", __name__)


@comment_management.route("/posts/<int:post_id>/comment", methods=["POST"])
def create_comment(post_id: int):
    data = request.form.to_dict()
    author_id = session.get("user_id")

    if not author_id:
        return jsonify({"error": "Login required"}), 401
    return core_create_comment(
        CommentDataCreate(
            content=data.get("content"),
            post_id=post_id,
            author_id=author_id,
        )
    )


@comment_management.route("/posts/<int:post_id>/comment", methods=["GET"])
def get_comments(post_id):
    return core_get_comments(post_id)
