#!/usr/bin/env python3
""" Module of Auth class
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """Auth class
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """returns False - path and excluded_paths will be used later
        """
        if path is None or excluded_paths is None or len(excluded_paths) == 0:
            return True
        for excluded_path in excluded_paths:
            if excluded_path.endswith('*'):
                if path.startswith(excluded_path[:-1]):
                    return False
            elif path == excluded_path or path == excluded_path.rstrip('/') \
                    or ''.join([path, '/']) == excluded_path:
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """returns None - request will be the Flask request object
        """
        if request is None:
            return None
        auth_header = request.headers.get('Authorization')

        if auth_header is None:
            return None
        return auth_header

    def current_user(self, request=None) -> TypeVar('User'):
        """returns None - request will be the Flask request object
        """
        return None
