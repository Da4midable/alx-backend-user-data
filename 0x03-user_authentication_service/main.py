#!/usr/bin/env python3
"""
Main file
"""
import requests


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


def register_user(email: str, password: str) -> None:
    
    """Registers a new user"""
    response = requests.post('http://127.0.0.1:5000/users', data={"email": email, "password": password})
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
    assert response.json() == {"email": email, "message": "user created"}, f"Unexpected payload: {response.json()}"

def log_in_wrong_password(email: str, password: str) -> None:
    """Tries to log in with the wrong password"""
    response = requests.post('http://127.0.0.1:5000/sessions', data={"email": email, "password": password})
    assert response.status_code == 401, f"Expected status code 401, got {response.status_code}"

def log_in(email: str, password: str) -> str:
    """Logs in with the correct credentials and returns session ID"""
    response = requests.post('http://127.0.0.1:5000/sessions', data={"email": email, "password": password})
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
    session_id = response.cookies.get('session_id')
    assert session_id is not None, "Session ID not found in cookies"
    return session_id

def profile_unlogged() -> None:
    """Tries to access the profile without being logged in"""
    response = requests.get('http://127.0.0.1:5000/profile')
    assert response.status_code == 403, f"Expected status code 403, got {response.status_code}"

def profile_logged(session_id: str) -> None:
    """Accesses the profile while logged in with session ID"""
    cookies = {'session_id': session_id}
    response = requests.get('http://127.0.0.1:5000/profile', cookies=cookies)
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"

def log_out(session_id: str) -> None:
    """Logs out using the session ID"""
    cookies = {'session_id': session_id}
    response = requests.delete('http://127.0.0.1:5000/sessions', cookies=cookies)
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"

def reset_password_token(email: str) -> str:
    """Requests a reset password token"""
    response = requests.post('http://127.0.0.1:5000/reset_password', data={"email": email})
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
    reset_token = response.json().get('reset_token')
    assert reset_token is not None, "Reset token not found in response"
    return reset_token

def update_password(email: str, reset_token: str, new_password: str) -> None:
    """Updates the user's password"""
    response = requests.put('http://127.0.0.1:5000/reset_password', data={
        "email": email, "reset_token": reset_token, "new_password": new_password
    })
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
    assert response.json() == {"email": email, "message": "Password updated"}, f"Unexpected payload: {response.json()}"


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
