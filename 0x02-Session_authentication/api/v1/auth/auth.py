#!/usr/bin/env python3
"""Authentications module"""

from flask import request
from typing import List, TypeVar
import os


class Auth:
    """Implement Auth class"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Require auth"""
        if path is None or excluded_paths is None or excluded_paths == []:
            return True

        if not path.endswith('/'):
            path = path + '/'

        for excluded_path in excluded_paths:
            if (excluded_path.endswith('*')
                    and path.startswith(excluded_path[:-1])):
                return False

            if path == excluded_path:
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """Authrization header"""
        if request is None:
            return None

        header = request.headers.get('Authorization')
        if not header:
            return None

        return header

    def current_user(self, request=None) -> TypeVar('User'):
        """Current user"""
        return None

    def session_cookie(self, request=None):
        """Returns value of the cookie"""
        if request:
            cookie_name = os.getenv('SESSION_NAME')
            return request.cookies.get(cookie_name)
