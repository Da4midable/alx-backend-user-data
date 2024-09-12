#!/usr/bin/env python3
"""
creates the Auth class for sesison and user authentication
"""

import uuid
import bcrypt
from user import User
from typing import Optional
from sqlalchemy.orm.exc import NoResultFound
from db import DB


def _hash_password(password: str) -> bytes:
    """
    returns bytes of a salted hash of the input password,
    hashed with bcrypt.hashpw
    """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password


def _generate_uuid() -> str:
    "generates a uuid4 module"
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """
    def __init__(self):
        """class constructor"""
        self._db = DB()

    def create_session(self, email: str) -> str:
        try:
            user_email = self._db.find_user_by(email=email)
            if user_email:
                user_email.session_id = _generate_uuid()
                return user_email.session_id
        except NoResultFound:
            return None

    def register_user(self, email: str, password: str) -> User:
        """registers user"""
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            hashed_password = _hash_password(password)
            new_user = self._db.add_user(email, hashed_password)
            return new_user

    def valid_login(self, email: str, password: str) -> bool:
        """checks if login is valid"""
        user = None
        try:
            user = self._db.find_user_by(email=email)
            if user:
                return bcrypt.checkpw(password.encode('utf-8'),
                                      user.hashed_password)
        except NoResultFound:
            return False
        return False

    def get_user_from_session_id(self, session_id:
                                 Optional[str]) -> Optional[User]:
        """finds user by session ID"""
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None
        return user

    def destroy_session(self, user_id: int) -> None:
        """finds user by id and destroys corresponding the session"""
        try:
            self._db.update_user(user_id, session_id=None)
        except NoResultFound:
            return None

    def get_reset_password_token(self, email: str) -> str:
        """generates reset password token"""
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError
        token = _generate_uuid()
        self._db.update_user(user.id, reset_token=token)
        return token

    def update_password(self, reset_token: str, password: str) -> None:
        """updates password and resets reset_token"""
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            hashed_password = _hash_password(password)
            self._db.update_user(user.id,
                                 user.hashed_password=hashed_password,
                                 user.reset_token=None)
        except NoResultFound:
            raise ValueError
