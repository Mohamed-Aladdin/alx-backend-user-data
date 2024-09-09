#!/usr/bin/env python3
"""App module
"""
from flask import Flask, jsonify, request, abort, redirect

from auth import Auth


app = Flask(__name__)

AUTH = Auth()


@app.route('/', methods=['GET'])
def index() -> str:
    """implements the GET / route
    """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def users() -> str:
    """implements the POST /users route
    """
    email = request.form.get('email')
    password = request.form.get('password')

    try:
        new_user = AUTH.register_user(email, password)
        return jsonify({"email": new_user.email, "message": "user created"})
    except Exception:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login() -> str:
    """implements the POST /sessions route
    """
    email = request.form.get('email')
    password = request.form.get('password')

    if AUTH.valid_login(email, password):
        session_id = AUTH.create_session(email)
        res = jsonify({"email": email, "message": "logged in"})
        res.set_cookie({'session_id': session_id})
        return res
    else:
        abort(401)


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout() -> str:
    """implements the DELETE /sessions route
    """
    session_id = request.cookies.get('session_id')
    fetched_user = AUTH.get_user_from_session_id(session_id)

    if not fetched_user:
        abort(403)
    AUTH.destroy_session(fetched_user.id)
    return redirect('/')


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile() -> str:
    """implements the GET /profile route
    """
    session_id = request.cookies.get('session_id')
    fetched_user = AUTH.get_user_from_session_id(session_id)

    if not fetched_user:
        abort(403)
    return jsonify({"email": fetched_user.email}), 200


@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def get_reset_password_token() -> str:
    """implements the POST /reset_password route
    """
    email = request.form.get('email')

    try:
        reset_token = AUTH.get_reset_password_token(email)
        return jsonify({"email": email, "reset_token": reset_token}), 200
    except Exception:
        abort(403)


@app.route('/reset_password', methods=['PUT'], strict_slashes=False)
def update_password() -> str:
    """implements the PUT /reset_password route
    """
    email = request.form.get('email')
    reset_token = request.form.get('reset_token')
    new_password = request.form.get('new_password')

    try:
        AUTH.update_password(reset_token, new_password)
        return jsonify({"email": email, "message": "Password updated"}), 200
    except Exception:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
