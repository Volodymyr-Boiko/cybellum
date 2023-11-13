from flask import Blueprint, request, session

from app.core.user_management import (
    UserLogin,
    UserRegister,
    core_user_login,
    core_user_logout,
    core_user_register,
)

user_management = Blueprint("user_management", __name__)


@user_management.route("/get_user/<user_id>")
def hello(user_id):
    return f"Hello, World!! {user_id}"


@user_management.route("/register", methods=["POST"])
def user_register():
    email = request.form.to_dict().get("email")
    username = request.form.to_dict().get("username")
    password_hash = request.form.to_dict().get("password_hash")
    user_register_data = UserRegister(
        email=email,
        username=username,
        password_hash=password_hash,
    )
    return core_user_register(user_register_data)


@user_management.route("/login", methods=["POST"])
def user_login():
    email = request.form.to_dict().get("email")
    password_hash = request.form.to_dict().get("password_hash")
    user_login_data = UserLogin(email=email, password_hash=password_hash)
    return core_user_login(user_login_data)


@user_management.route("/logout", methods=["POST"])
def user_logout():
    return core_user_logout()
