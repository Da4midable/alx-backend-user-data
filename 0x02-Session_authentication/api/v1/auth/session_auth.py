#!/usr/bin/env python3
"""module for creating a SessionAuth instance"""
from api.v1.auth.auth import Auth
from models.user import User
import uuid


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

    def destroy_session(self, request=None):
        """deletes the user session / logs out"""
        if request == 'None':
            return False
        sess_id = self.session_cookie(request)
        if sess_id is None:
            return False
        user_id = self.user_id_for_session_id(sess_id)
        if user_id is None:
            return False
        self.user_id_by_session_id.pop(user_id, None)
        return True
