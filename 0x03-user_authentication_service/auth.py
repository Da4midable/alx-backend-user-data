#!/usr/bin/env python3
"""
defines a _hash_password method that takes in
a password string arguments and returns bytes.
"""

import uuid
import bcrypt
from user import User
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
