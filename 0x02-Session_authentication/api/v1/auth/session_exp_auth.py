#!/usr/bin/env python3
"""
Module of Session Expiry Auth
"""
import os
from flask import request
from .session_auth import SessionAuth
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """Session Expiry Auth class
    """

    def __init__(self):
        """Initialize
        """
        super().__init__()
        try:
            self.session_duration = int(os.getenv('SESSION_DURATION', '0'))
        except Exception:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """creates a Session ID for a user_id
        """
        if user_id is None or not isinstance(user_id, str):
            return None
        session_id = super().create_session(user_id)
        self.user_id_by_session_id[session_id] = {
            'user_id': user_id,
            'created_at': datetime.now()
        }
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Retrieves the user id of the user associated with
        a given session id.
        """
        if session_id is None or not isinstance(session_id, str):
            return None
        if not super().user_id_for_session_id(session_id):
            return None
        session_dictionary = self.user_id_by_session_id[session_id]

        if self.session_duration <= 0:
            return session_dictionary['user_id']
        if 'created_at' not in session_dictionary:
            return None
        time_now = datetime.now()
        time_range = timedelta(seconds=self.session_duration)
        expiry_time = session_dictionary['created_at'] + time_range

        if expiry_time < time_now:
            return None
        return session_dictionary['user_id']
