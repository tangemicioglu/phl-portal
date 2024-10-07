from flask import jsonify, request, url_for
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
from app.api import bp
from app import db
from app.database.models import User
from app.api.errors import error_response, bad_request

basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth()


@basic_auth.verify_password
def verify_password(username, password):
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        return user


@basic_auth.error_handler
def basic_auth_error(status):
    return error_response(status)


@token_auth.verify_token
def verify_token(token):
    return User.check_token(token) if token else None


@token_auth.error_handler
def token_auth_error(status):
    return error_response(status)


@bp.route("/users/<int:id>", methods=["GET"])
@token_auth.login_required
def get_user(id):
    print("get users")
    return jsonify(User.query.get_or_404(id).to_dict())


@bp.route("/users", methods=["POST"])
def create_user():
    data = request.get_json() or {}
    if "username" not in data or "email" not in data or "password" not in data:
        return bad_request("must include username, email and password fields")
    if User.query.filter_by(username=data["username"]).first():
        return bad_request("Please use a different username.")
    if User.query.filter_by(email=data["email"]).first():
        return bad_request("Please use a different email address.")
    user = User()
    user.from_dict(data, is_new_user=True)
    db.session.add(user)
    db.session.commit()
    response = jsonify(user.to_dict())
    response.status_code = 201
    response.headers["Location"] = url_for("api.get_user", id=user.id)
    return response
