#!/usr/bin/env python3
"""Defines session_auth module"""

from .auth import Auth
from models.user import User
import uuid


class SessionAuth(Auth):
    """Implement SessionAuth class"""
    user_id_by_session_id = {}

    def __init__(self) -> None:
        super().__init__()

    def create_session(self, user_id: str = None) -> str:
        """Creates Id from the user_id"""
        if not user_id or not isinstance(user_id, str):
            return None

        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id

        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Returns user_id based on session_id"""
        if not session_id or not isinstance(session_id, str):
            return None

        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """Returns user instance"""
        session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id)

        user = User.get(user_id)
        return user

    def destroy_session(self, request=None):
        """Destroy the user session"""
        session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id)
        if user_id is None:
            return False

        if session_id in self.user_id_by_session_id:
            del self.user_id_by_session_id[session_id]
        return True
