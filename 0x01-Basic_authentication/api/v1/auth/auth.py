#!/usr/bin/env python3
"""module creates a class to manage the API authentication"""

from flask import request
from typing import TypeVar, List


class Auth:
    """class manages the API authentication"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """to validate authentication"""
        return False

    def authorization_header(self, request=None) -> str:
        """to authenticate header"""
        return request

    def current_user(self, request=None) -> TypeVar('User'):
        """to retrieve current user"""
        return request
