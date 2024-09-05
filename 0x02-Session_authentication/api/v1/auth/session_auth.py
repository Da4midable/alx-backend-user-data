#!/usr/bin/env python3
"""module for creating a SessionAuth instance"""
from api.v1.auth.auth import Auth
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
