import dataclasses

from flask import jsonify
from flask import session as flask_session

from app.database.models import Session, User


@dataclasses.dataclass
class UserLogin:
    email: str
    password_hash: str


@dataclasses.dataclass
class UserRegister(UserLogin):
    username: str


def core_user_register(user_register_data: UserRegister):
    if (
        not user_register_data.username
        or not user_register_data.email
        or not user_register_data.password_hash
    ):
        return jsonify({"error": "Invalid input data"}), 400
    try:
        new_user = User(
            username=user_register_data.username,
            email=user_register_data.email,
            password_hash=user_register_data.password_hash,
        )
        session = Session()
        session.add(new_user)
        session.commit()
        return jsonify({"message": "User registered successfully"}), 201
    except Exception as e:
        return jsonify({"error": f"{e}"}), 400


def core_user_login(user_login_data: UserLogin):
    session = Session()
    user = (
        session.query(User)
        .filter(User.email == user_login_data.email)
        .filter(User.password_hash == user_login_data.password_hash)
        .first()
    )
    if not user:
        return jsonify({"message": "User login failed"}), 401
    flask_session["user_id"] = user.id
    return jsonify({"message": "User login successfully"}), 200


def core_user_logout():
    if "user_id" in flask_session:
        flask_session.pop("user_id")
    return jsonify({"message": "User logout successfully"}), 200
