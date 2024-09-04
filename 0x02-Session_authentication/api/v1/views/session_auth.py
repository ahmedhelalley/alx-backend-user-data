#!/usr/bin/env python3
"""Defines session_auth view"""


from api.v1.views import app_views
from flask import jsonify, request, abort
from models.user import User
import os


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def authorize_session() -> str:
    """Implement login route"""
    email = request.form.get('email')
    password = request.form.get('password')

    if not email:
        return jsonify({"error": "email missing"}), 400

    if not password:
        return jsonify({"error": "password missing"}), 400

    users = User().search({'email': email})
    if not users:
        return jsonify({"error": "no user found for this email"}), 404

    user = users[0]

    is_valid_pwd = user.is_valid_password(password)

    if not is_valid_pwd:
        return jsonify({"error": "wrong password"}), 401

    from api.v1.app import auth
    sessionId = auth.create_session(user.id)
    user_response = jsonify(user.to_json())
    user_response.set_cookie(os.getenv('SESSION_NAME'), sessionId)

    return user_response


@app_views.route('/auth_session/logout',
                 methods=['DELETE'],
                 strict_slashes=False)
def logout():
    """Implement logout route"""
    from api.v1.app import auth

    if not auth.destroy_session(request):
        abort(404)

    return jsonify({}), 200
