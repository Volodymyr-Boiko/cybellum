import dataclasses
import datetime
from typing import List

from flask import jsonify

from app.database.models import Post, Session, User


@dataclasses.dataclass
class BlogPostDataCreate:
    title: str
    content: str
    author_id: int


@dataclasses.dataclass
class BlogPostData(BlogPostDataCreate):
    created_at: datetime.datetime


def core_create_post(blog_post_data: BlogPostDataCreate):
    if (
        not blog_post_data.title
        or not blog_post_data.content
        or not blog_post_data.author_id
    ):
        return jsonify({"error": "Title, content, and author_id are required"}), 400

    session = Session()
    user = session.query(User).filter(User.id == blog_post_data.author_id).first()
    if not user:
        session.close()
        return jsonify({"error": "Author does not exist"}), 404

    post = Post(
        title=blog_post_data.title,
        content=blog_post_data.content,
        author_id=blog_post_data.author_id,
    )

    session.add(post)
    session.commit()
    session.close()

    return jsonify({"message": "Post created successfully"}), 201


def core_get_posts() -> List[BlogPostData]:
    session = Session()
    posts = session.query(Post).all()
    blog_posts = [
        BlogPostData(
            title=post.title,
            content=post.content,
            author_id=post.author_id,
            created_at=post.created_at,
        )
        for post in posts
    ]
    return blog_posts


def core_get_post(post_id: int) -> dict:
    session = Session()
    post = session.query(Post).filter(Post.id == post_id).first()
    if not post:
        return jsonify({"error": "Post does not exist"}), 404
    blog_post = BlogPostData(
        title=post.title,
        content=post.content,
        author_id=post.author_id,
        created_at=post.created_at,
    )
    return dataclasses.asdict(blog_post)
