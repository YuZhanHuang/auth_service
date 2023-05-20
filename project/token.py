from datetime import timedelta

from flask_jwt_extended import create_access_token


def jwt_token(role, user_id, expires_delta=timedelta(hours=8)):
    return create_access_token(identity={
        'role': role,
        'user_id': str(user_id)
    }, expires_delta=expires_delta)
