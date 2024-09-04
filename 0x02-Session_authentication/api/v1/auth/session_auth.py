#!/usr/bin/env python3
"""
Module of Session Auth
"""
from uuid import uuid4
from .auth import Auth
from models.user import User


class SessionAuth(Auth):
    """Session Auth class
    """

    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """creates a Session ID for a user_id
        """
        if user_id is None or not isinstance(user_id, str):
            return None
        session_id = uuid4()
        self.user_id_by_session_id[str(session_id)] = user_id
        return str(session_id)

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """returns a User ID based on a Session ID
        """
        if session_id is None or not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """returns a User instance based on a cookie value
        """
        cookie = self.session_cookie(request)
        user_id = self.user_id_for_session_id(cookie)
        return User.get(user_id)

    def destroy_session(self, request=None):
        """deletes the user session / logout
        """
        if request is None:
            return False
        cookies = self.session_cookie(request)

        if cookies is None:
            return False
        user_id = self.user_id_for_session_id(cookies)
        if user_id is None:
            return False
        del self.user_id_by_session_id[cookies]
        return True
