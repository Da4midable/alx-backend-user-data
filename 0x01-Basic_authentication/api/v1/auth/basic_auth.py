#!/usr/bin/env python3
"""module creates a BasicAuth class"""

from api.v1.auth.auth import Auth
import base64


class BasicAuth(Auth):
    """class creates BasicAuth instance"""
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """
        Uses the Base64 part of the Authorization
        header for a basic authentication
        """
        if authorization_header is None:
            return None
        if type(authorization_header) is not str:
            return None
        if not authorization_header.startswith("Basic "):
            return None
        return authorization_header.strip("Basic ")

    def decode_base64_authorization_header(self,
                                           base64_authorization_header:
                                           str) -> str:
        """decodes value of a Base64 string"""
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            decoded_bytes = base64.b64decode(base64_authorization_header)
            return decoded_bytes.decode('utf-8')
        except Exception:
            return None
