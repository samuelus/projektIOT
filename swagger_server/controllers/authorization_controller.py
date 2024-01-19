import jwt
from jwt import ExpiredSignatureError, DecodeError
from werkzeug.exceptions import Unauthorized
from database import cryptography

"""
controller generated to handled auth operation described at:
https://connexion.readthedocs.io/en/latest/security.html
"""


def check_bearerAuth(token):
    try:
        return jwt.decode(token, cryptography.SALT, algorithms=["HS256"])
    except ExpiredSignatureError:
        raise Unauthorized
    except DecodeError:
        raise Unauthorized
    except Exception:
        raise Unauthorized
