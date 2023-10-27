from flask.testing import FlaskClient
from pytest_mock import MockerFixture

from app.core.blog import BlogPostDataCreate


def test_create_blog(client: FlaskClient, mocker: MockerFixture):
    with client.session_transaction() as session:
        session["user_id"] = 1
    create_post_mock = mocker.patch(
        "app.api.blog_post_management.blog.core_create_post", return_value={}
    )
    client.post(
        "/create_post",
        data={"title": "Title", "content": "Content"},
    )
    create_post_mock.assert_called_once_with(
        BlogPostDataCreate(title="Title", content="Content", author_id=1)
    )
