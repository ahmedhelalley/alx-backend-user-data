#!/usr/bin/env python3
"""Defines main module"""

import requests

EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"
HOST_URL = "http://0.0.0.0:5000"


def register_user(email: str, password: str) -> None:
    """Test register user"""
    url = f"{HOST_URL}/users"
    request_body = {
        'email': email,
        'password': password
    }

    response = requests.post(url, data=request_body)
    assert response.status_code == 200
    assert response.json() == {'email': email, 'message': 'user created'}

    response = requests.post(url, data=request_body)
    assert response.status_code == 400
    assert response.json() == {"message": "email already registered"}


def log_in_wrong_password(email: str, password: str) -> None:
    """Test login with wrong password"""
    url = f"{HOST_URL}/sessions"
    request_body = {
        'email': email,
        'password': password
    }

    response = requests.post(url, data=request_body)
    response.status_code == 401


def log_in(email: str, password: str) -> str:
    """Test login with happy scenario"""
    url = f"{HOST_URL}/sessions"
    request_body = {
        'email': email,
        'password': password
    }

    response = requests.post(url, data=request_body)
    session_id = response.cookies.get('session_id')
    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "logged in"}
    assert session_id is not None
    assert isinstance(session_id, str)

    return session_id


def profile_unlogged() -> None:
    """Test getting user profile without session_id"""
    url = f"{HOST_URL}/profile"
    response = requests.get(url)
    assert response.status_code == 403


def profile_logged(session_id: str) -> None:
    """Test getting a logged in profile"""
    url = f"{HOST_URL}/profile"
    request_cookies = {
        'session_id': session_id
    }
    response = requests.get(url, cookies=request_cookies)

    assert response.status_code == 200
    assert response.json().get('email')


def log_out(session_id: str) -> None:
    """Test logout"""
    url = f"{HOST_URL}/sessions"
    request_cookies = {
        'session_id': session_id
    }
    response = requests.delete(url, cookies=request_cookies)

    assert response.status_code == 200
    assert response.json() == {"message": "Bienvenue"}


def reset_password_token(email: str) -> str:
    """Test getting the reset token"""
    url = f"{HOST_URL}/reset_password"
    request_body = {'email': email}
    response = requests.post(url, data=request_body)
    reset_token = response.json().get('reset_token')

    assert response.status_code == 200
    assert response.json().get('email') == email
    assert reset_token is not None
    assert isinstance(reset_token, str)

    return reset_token


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """Test update password"""
    url = f"{HOST_URL}/reset_password"
    request_body = {
        'email': email,
        'reset_token': reset_token,
        'new_password': new_password
    }
    response = requests.put(url, data=request_body)

    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "Password updated"}


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
