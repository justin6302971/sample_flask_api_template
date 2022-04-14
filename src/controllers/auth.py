from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from src.constants.http_status_codes import *
import validators

from src.db.database import User, db
# from sqlalchemy import or_

from flask_jwt_extended import get_jwt_identity, jwt_required, create_access_token, create_refresh_token

auth = Blueprint("auth", __name__, url_prefix="/api/v1/auth")


@auth.post("/register")
def register():
    username = request.json.get('username', '')
    email = request.json.get('email', '')
    password = request.json.get('password', '')

    if len(password) < 6:
        return jsonify({'error': "password is too short"}), HTTP_400_BAD_REQUEST

    if len(username) < 3:
        return jsonify({'error': "username is too short"}), HTTP_400_BAD_REQUEST

    if not username.isalnum() or " " in username:
        return jsonify({'error': "username should be alphanumeric without spaces"}), HTTP_400_BAD_REQUEST

    if not validators.email(email):
        return jsonify({'error': "email is not valid"}), HTTP_400_BAD_REQUEST

    exist_useremail = User.query.filter_by(email=email).first()

    if exist_useremail is not None:
        return jsonify({'error': "email is used"}), HTTP_409_CONFLICT

    exist_username = User.query.filter_by(username=username).first()

    if exist_username is not None:
        return jsonify({'error': "username is used"}), HTTP_409_CONFLICT

    pwd_hash = generate_password_hash(password)

    user = User(username=username, password=pwd_hash, email=email)

    db.session.add(user)
    db.session.commit()

    return jsonify(
        {
            'isSuccess': True,
            "message": "user created successfully",
            "data": {
                username: username,
                email: email
            }
        }), HTTP_201_CREATED


@auth.post("/login")
def login():
    email = request.json.get('email', '')
    password = request.json.get('password', '')

    user = User.query.filter_by(email=email).first()

    if user is None:
        return jsonify({'error': "wrong credentials"}), HTTP_401_UNAUTHORIZED

    is_pass_correct = check_password_hash(user.password, password)

    if not is_pass_correct:
        return jsonify({'error': "wrong credentials"}), HTTP_401_UNAUTHORIZED

    access_token = create_access_token(identity=user.id)
    refresh_token = create_refresh_token(identity=user.id)

    return jsonify(
        {
            "access_token": access_token,
            "refresh_token": refresh_token
        }), HTTP_200_OK


@auth.get("/me")
@jwt_required()
def me():
    user_id = get_jwt_identity()

    user = User.query.filter_by(id=user_id).first()

    return jsonify(
        {
            "username": user.username,
            "email": user.email
        }), HTTP_200_OK


@auth.post('/token/refresh')
@jwt_required(refresh=True)
def refresh_token():
    identity = get_jwt_identity()
    access_token = create_access_token(identity)

    return jsonify(
        {
            "access_token": access_token
        }), HTTP_200_OK
