#!/usr/bin/env python3
"""Module sets up a basic Flask app."""

from flask import Flask, jsonify, request, Response, abort
from auth import Auth


AUTH = Auth()
app = Flask(__name__)


@app.route('/', methods=['GET'], strict_slashes=False)
def simple_message():
    """
    return a JSON payload of the form:

    {"message": "Bienvenue"}
    """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'])
def users() -> Response:
    
    if request.method == 'POST':
        unstripped_email = request.form.get('email')
        unstripped_password = request.form.get('password')

        email = unstripped_email.strip()
        password = unstripped_password.strip()

    try:
        AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"})
    except Exception:
        return jsonify({"message": "email already registered"})
    else:
        abort(400)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
