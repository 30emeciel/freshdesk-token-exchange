from datetime import datetime, timedelta
from os import environ

import jwt
import requests
from dotmap import DotMap

FRESHDESK_SHARED_SECRET_KEY = environ["FRESHDESK_SHARED_SECRET_KEY"]


def from_request(request):
    """Responds to any HTTP request.
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        The response text or any set of values that can be turned into a
        Response object using
        `make_response <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>`.
    """

    # Set CORS headers for preflight requests
    if request.method == 'OPTIONS':
        # Allows GET requests from any origin with
        # Authorization header
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST',
            'Access-Control-Allow-Headers': 'content-type',
            'Access-Control-Max-Age': '3600',
        }
        return '', 204, headers

    from flask import abort
    if request.method != 'POST':
        return abort(405)

    request_data = DotMap(request.get_json())
    access_token = request_data.access_token
    freshdesk_token = convert_auth0_token_to_freshdesk_token(access_token)
    headers = {
        'Access-Control-Allow-Origin': '*',
    }
    return ({
                "freshdesk_token": freshdesk_token
            }, 200, headers)


def convert_auth0_token_to_freshdesk_token(auth0_token):
    # valid auth0_token and get user_profile
    up = get_user_profile(auth0_token)
    return get_freshdesk_token(up.name, up.email)


def get_freshdesk_token(name, email):
    payload = {
        "name": name,
        "email": email,
        "exp": int((datetime.now() + timedelta(hours=2)).timestamp())
    }
    token = jwt.encode(payload, FRESHDESK_SHARED_SECRET_KEY, algorithm='HS256')
    return token


def get_user_profile(token):
    headers = {
        "Authorization": f"Bearer {token}"
    }

    req = requests.get("https://paxid.eu.auth0.com/userinfo", headers=headers)
    req.raise_for_status()
    resp = req.json()
    return DotMap(resp)
