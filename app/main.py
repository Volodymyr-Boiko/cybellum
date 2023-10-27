from flask import Flask

from app.api.blog_post_management.blog import blog_post_management
from app.api.comment_management.comment import comment_management
from app.api.user_management.user_management import user_management

# from settings import get_settings
from app.settings import get_settings

settings = get_settings()

app = Flask(__name__)
app.secret_key = settings.secret_key


app.register_blueprint(user_management)
app.register_blueprint(blog_post_management)
app.register_blueprint(comment_management)


@app.route("/")
def hello():
    return "Hello, World!"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
