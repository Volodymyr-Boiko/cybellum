from flask.testing import FlaskClient
from pytest_mock import MockerFixture

from app.core.comment import CommentDataCreate


def test_create_comment(client: FlaskClient, mocker: MockerFixture):
    with client.session_transaction() as session:
        session["user_id"] = 1
    create_comment_mock = mocker.patch(
        "app.api.comment_management.comment.core_create_comment", return_value={}
    )
    client.post(
        "/posts/1/comment",
        data={"content": "Content"},
    )
    create_comment_mock.assert_called_once_with(
        CommentDataCreate(content="Content", author_id=1, post_id=1)
    )
