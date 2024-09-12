#!/usr/bin/env python3
"""Module sets up a basic Flask app."""

from flask import Flask, jsonify, request, Response, abort, make_response
from flask import redirect
from auth import Auth


AUTH = Auth()
app = Flask(__name__)


@app.route('/')
def simple_message() -> Response:
    """
    return a JSON payload of the form:

    {"message": "Bienvenue"}
    """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'])
def users() -> Response:
    """
    Registers user
    """
    email = request.form.get('email')
    password = request.form.get('password')

    try:
        AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'])
def login():
    """creates a new session for the user, store it the session ID as a cookie
    with key "session_id" on the response
    If login information is incorrect, flask aborts with a 401 HTTP status.
    Return:
    a JSON payload of the form
    """
    email = request.form.get('email')
    password = request.form.get('password')

    if not AUTH.valid_login(email, password):
        abort(401)

    session_id = AUTH.create_session(email)
    response = make_response(jsonify({"email": email, "message": "logged in"}))
    response.set_cookie('session_id', session_id)
    return response


@app.route('/sessions', methods=['DELETE'])
def logout():
    """Logout user by deleting session"""
    session_id = request.cookies.get('session_id')

    if session_id is None:
        abort(403)

    user = AUTH.get_user_from_session_id(session_id)

    if not user:
        abort(403)

    AUTH.destroy_session(user.id)
    response = redirect('/')
    response.delete_cookie('session_id')
    return response


@app.route('/profile', methods=['GET'])
def profile():
    """
    Finds user with session ID and returns 200 HTTP status.
    Aborts otherwise.
    """
    session_id = request.cookies.get('session_id')
    if session_id:
        user = AUTH.get_user_from_session_id(session_id)
        if user:
            return jsonify({"email": user.email}), 200
        abort(403)
    abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
