#!/usr/bin/env python3
"""Defines session_db_auth module"""

from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from datetime import datetime, timedelta


class SessionDBAuth(SessionExpAuth):
    """Implement SessionDBAuth class"""
    def create_session(self, user_id=None):
        """Creates a sessionId and stores it to a file"""
        session_id = super().create_session(user_id)
        if not session_id:
            return None

        user_session = UserSession(user_id=user_id, session_id=session_id)
        user_session.save()

        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Returns user_id by requesting UserSession based on session_id"""
        if not session_id or not isinstance(session_id, str):
            return None

        users = UserSession().search({'session_id': session_id})
        if not users:
            return None

        user = users[0]
        if not self.is_session_expired(user.created_at):
            return None

        return user.user_id

    def is_session_expired(self, created_at):
        """Checks if a session is expired"""
        if self.session_duration <= 0:
            return True

        expiration_time = created_at + timedelta(seconds=self.session_duration)
        return expiration_time >= datetime.now()

    def destroy_session(self, request=None):
        """Destroys UserSession based on the Session_ID from request cookie"""
        session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id)
        if user_id is None:
            return False

        users = UserSession.search({'session_id': session_id})
        if not users:
            return False

        user = users[0]
        user.remove()
        UserSession.save_to_file()

        return True
