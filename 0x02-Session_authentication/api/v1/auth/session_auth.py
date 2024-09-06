#!/usr/bin/env python3
"""module for creating a SessionAuth instance"""
from api.v1.auth.auth import Auth
from api.v1.views import app_views
from models.user import User
import uuid
import os
from flask import Flask, request, jsonify


class SessionAuth(Auth):
    """creates a SessionAuth instance"""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """method creates session ID"""
        if user_id is None or not isinstance(user_id, str):
            return None
        sess_id = str(uuid.uuid4())
        self.user_id_by_session_id[sess_id] = user_id
        return sess_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """instance method returns a User ID based on a Session ID"""
        if session_id is None or not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """returns User instance based on cookie value"""
        session_id = self.session_cookie(request)
        if session_id is None:
            return None
        user_id = self.user_id_for_session_id(session_id)
        if user_id is None:
            return None
        user = User.get(user_id)
        return user


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def user_session():
    """
    Handles POST request to /auth_session/login for session authentication
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
