#!/usr/bin/env python3
"""
Module of Session DB Auth
"""
from datetime import datetime, timedelta
from models.user_session import UserSession
from .session_exp_auth import SessionExpAuth


class SessionDBAuth(SessionExpAuth):
    """Session DB Auth class
    """

    def create_session(self, user_id=None):
        """creates a Session ID for a user_id
        """
        if user_id is None or not isinstance(user_id, str):
            return None
        session_id = super().create_session(user_id)

        session_dictionary = {
            'user_id': user_id,
            'session_id': session_id
        }
        user_session = UserSession(**session_dictionary)
        user_session.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Retrieves the user id of the user associated with
        a given session id.
        """
        if session_id is None or not isinstance(session_id, str):
            return None
        session_list = UserSession.search({'session_id': session_id})

        if session_list is None or len(session_list) <= 0:
            return None
        time_now = datetime.now()
        time_range = timedelta(seconds=self.session_duration)
        expiry_time = session_list[0].created_at + time_range

        if expiry_time < time_now:
            return None
        return session_list[0].user_id

    def destroy_session(self, request=None):
        """deletes the user session / logout
        """
        if request is None:
            return False
        session_id = self.session_cookie(request)

        if session_id is None:
            return False
        session_list = UserSession.search({'session_id': session_id})

        if session_list is None or len(session_list) == 0:
            return False
        session_list[0].remove()
        return True
