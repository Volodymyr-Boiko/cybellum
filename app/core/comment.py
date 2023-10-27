import dataclasses
import datetime

from flask import jsonify
from flask import session as flask_session

from app.database.models import Comment, Post, Session, User


@dataclasses.dataclass
class CommentDataCreate:
    content: str
    author_id: int
    post_id: int


@dataclasses.dataclass
class CommentData(CommentDataCreate):
    created_at: datetime.datetime


def core_create_comment(comment_data: CommentDataCreate):
    if (
        not comment_data.content
        or not comment_data.post_id
        or not comment_data.author_id
    ):
        return jsonify({"error": "Title, content, and author_id are required"}), 400

    session = Session()
    user = session.query(User).filter(User.id == comment_data.author_id).first()
    if not user:
        session.close()
        return jsonify({"error": "Author does not exist"}), 404

    post = session.query(Post).filter(Post.id == comment_data.post_id).first()
    if not post:
        session.close()
        return jsonify({"error": "Post does not exist"}), 404
    comment = Comment(
        content=comment_data.content,
        author_id=comment_data.author_id,
        post_id=comment_data.post_id,
    )

    session.add(comment)
    session.commit()
    session.close()

    return jsonify({"message": "Comment created successfully"}), 201


def core_get_comments(post_id: int):
    author_id = flask_session.get("user_id")

    if not author_id:
        return jsonify({"error": "Login required"}), 401
    session = Session()
    comments = session.query(Comment).filter(Comment.post_id == post_id).all()
    if not comments:
        return jsonify({"error": "Comments do not exist"}), 404
    comments_data = [
        CommentData(
            content=comment.content,
            author_id=comment.author_id,
            post_id=comment.post_id,
            created_at=comment.created_at,
        )
        for comment in comments
    ]
    return comments_data
