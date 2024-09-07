#!/usr/bin/env python3
"""
Module for a route that handles POST request
to /auth_session/login for session authentication
"""

from flask import request, jsonify, abort
from models.user import User
from api.v1.views import app_views
from api.v1.app import auth
import os


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login():
    """
    function handles POST request to /auth_session/login
    for session authentication
    """
    email = request.form.get('email')
    password = request.form.get('password')

    if not email:
        return jsonify({"error": "email missing"}), 400
    if not password:
        return jsonify({"error": "password missing"}), 400
    users = User.search({'email': email})
    if not users or len(users) == 0:
        return jsonify({"error": "no user found for this email"}), 404

    user = users[0]

    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    from api.v1.app import auth

    session_id = auth.create_session(user.id)
    response = jsonify(user.to_json())
    session_name = os.getenv('SESSION_NAME')
    if session_name:
        response.set_cookie(session_name, session_id)

    return response


@app_views.route('/api/v1/auth_session/logout',
                 methods=['DELETE'], strict_slashes=False)
def logout():
    """
    function handles DELETE request to /auth_session/logout
    """
    if not auth.destroy_session(request):
        abort(404)
    return jsonify({}), 200
