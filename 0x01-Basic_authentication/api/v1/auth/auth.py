#!/usr/bin/env python3
"""module creates a class to manage the API authentication"""

from flask import request
from typing import TypeVar, List


class Auth:
    """class manages the API authentication"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        validates authentication with support for wildcard in excluded paths
        """
        if path is None or excluded_paths is None or not excluded_paths:
            return True
        for excluded_path in excluded_paths:
            if excluded_path.endswith('*'):
                if path.startswith(excluded_path[:-1]):
                    return False
            elif path == excluded_path or path == excluded_path.rstrip('/'):
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """to authenticate header"""
        if request is None:
            return None
        authorization = request.headers.get('Authorization')
        if not authorization:
            return None
        return authorization

    def current_user(self, request=None) -> TypeVar('User'):
        """to retrieve current user"""
        return request
