#!/usr/bin/env python3
"""Defines basic_auth module"""

from .auth import Auth
from models.user import User
import base64
from typing import TypeVar


class BasicAuth(Auth):
    """Implement BasicAuth class"""
    def __init__(self) -> None:
        super().__init__()

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """Extract base64 from the header"""
        if (authorization_header is None
                or type(authorization_header) is not str
                or not authorization_header.startswith('Basic ')):
            return None

        return authorization_header[6:]

    def decode_base64_authorization_header(
            self,
            base64_authorization_header: str
            ) -> str:
        """Decode base64 header"""
        if (base64_authorization_header is None
                or type(base64_authorization_header) is not str):
            return None

        try:
            decoded_bytes = base64.b64decode(base64_authorization_header)
            return decoded_bytes.decode('utf-8')
        except UnicodeDecodeError:
            return None

    def extract_user_credentials(
            self,
            decoded_base64_authorization_header: str
            ) -> (str, str):
        """Extract username and password"""
        if (decoded_base64_authorization_header is None
                or not isinstance(decoded_base64_authorization_header, str)):
            return None, None

        user_credentials = decoded_base64_authorization_header.split(':', 1)

        if len(user_credentials) != 2:
            return None, None

        return tuple(user_credentials)

    def user_object_from_credentials(self, user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """Get user using email and password"""
        if user_email is None or not isinstance(user_email, str):
            return None

        if user_pwd is None or not isinstance(user_pwd, str):
            return None

        users = User().search({'email': user_email})

        if not users:
            return None

        user = users[0]

        is_valid_pwd = user.is_valid_password(user_pwd)

        if not is_valid_pwd:
            return None

        return user

    def current_user(self, request=None) -> TypeVar('User'):
        """Get the authorized user"""
        auth_header = self.authorization_header(request)
        if not auth_header:
            return None

        base64_header = self.extract_base64_authorization_header(auth_header)
        if not base64_header:
            return None

        decoded_header = self.decode_base64_authorization_header(base64_header)
        if not decoded_header:
            return None

        email, password = self.extract_user_credentials(decoded_header)
        if not email or not password:
            return None

        return self.user_object_from_credentials(email, password)
