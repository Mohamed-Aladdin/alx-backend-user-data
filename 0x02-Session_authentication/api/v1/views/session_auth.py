#!/usr/bin/env python3
""" Module of Session Auth views
"""
import os
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def session_auth():
    """Session Auth handler
    """
    email = request.form.get('email')

    if email is None or len(email) == 0:
        return jsonify({"error": "email missing"}), 400
    password = request.form.get('password')

    if password is None or len(password) == 0:
        return jsonify({"error": "password missing"}), 400

    user_list = User.search({'email': email})

    if user_list is None or len(user_list) == 0:
        return jsonify({"error": "no user found for this email"}), 404
    for user in user_list:
        if user.is_valid_password(password):
            from api.v1.app import auth
            session_id = auth.create_session(user.id)
            res = jsonify(user.to_json())
            cookies = os.getenv('SESSION_NAME')
            res.set_cookie(cookies, session_id)
            return res
    return jsonify({"error": "wrong password"}), 401


@app_views.route('/auth_session/logout',
                 methods=['DELETE'], strict_slashes=False)
def logout():
    """Logout handler
    """
    from api.v1.app import auth

    if auth.destroy_session(request):
        return jsonify({}), 200
    abort(404)
