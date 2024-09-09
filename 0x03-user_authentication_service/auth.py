#!/usr/bin/env python3
"""Auth module
"""
import bcrypt
import uuid
from sqlalchemy.orm.exc import NoResultFound

from db import DB
from user import User


def _hash_password(password: str) -> str:
    """method that takes in a password string arguments
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def _generate_uuid() -> str:
    """should return a string representation of a new UUID
    """
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """should take mandatory email and password
        string arguments and return a User object
        """
        try:
            self._db.find_user_by(email=email)
        except NoResultFound:
            return self._db.add_user(email, _hash_password(password))
        else:
            raise ValueError('User {} already exists'.format(email))

    def valid_login(self, email: str, password: str) -> bool:
        """It should expect email and password
        required arguments and return a boolean
        """
        try:
            fetched_user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False
        return bcrypt.checkpw(password.encode('utf-8'),
                              fetched_user.hashed_password)

    def create_session(self, email: str) -> str:
        """The method should find the user corresponding to the email,
        generate a new UUID and store it in the database as
        the user’s session_id, then return the session ID
        """
        try:
            fetched_user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            fetched_user.session_id = session_id
            return fetched_user.session_id
        except NoResultFound:
            return None


    def get_user_from_session_id(self, session_id: str) -> User:
        """If the session ID is None or no user is found,
        return None. Otherwise return the corresponding user
        """
        if session_id is None:
            return None
        try:
            fetched_user = self._db.find_user_by(session_id=session_id)
            return fetched_user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """The method updates the corresponding user’s session ID to None
        """
        try:
            fetched_user = self._db.find_user_by(id=user_id)
        except NoResultFound:
            return None
        else:
            fetched_user.session_id = None
            return None

    def get_reset_password_token(self, email: str) -> str:
        """Find the user corresponding to the email.
        If the user does not exist, raise a ValueError exception.
        If it exists, generate a UUID and update the user’s
        reset_token database field. Return the token
        """
        try:
            fetched_user = self._db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError
        else:
            fetched_user.reset_token = _generate_uuid()
            return fetched_user.reset_token

    def update_password(self, reset_token: str, password: str) -> None:
        """Use the reset_token to find the corresponding user.
        If it does not exist, raise a ValueError exception.
        Otherwise, hash the password and update the user’s hashed_password
        with the new hashed password and the reset_token field to None"""
        try:
            fetched_user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            raise ValueError
        else:
            fetched_user.hashed_password = _hash_password(password)
            fetched_user.reset_token = None
            return None
