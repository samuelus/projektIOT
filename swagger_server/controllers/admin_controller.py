import datetime

import connexion
import jwt
from flask import make_response

from database import db_manager, cryptography
from swagger_server.models.inline_response200 import InlineResponse200


def login_admin(body):
    """Log in to the system.

    This endpoint authenticates users and provides a JWT token for accessing secure endpoints. # noqa: E501

    :param body:
    :type body: dict | bytes

    :rtype: InlineResponse200
    """
    database = db_manager.DbManager
    admins = database.read_all_administratorzy()
    if connexion.request.is_json:
        login = body.get('username')
        password = body.get('password')

        if not login or not password:
            return 'Missing username or password', 400
        admin = next((admin for admin in admins if admin.login == login), None)
        if admin is not None and cryptography.verify_password(password, admin.hash_hasla):
            token = jwt.encode({
                'public_id': admin.login,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
            }, cryptography.SALT, algorithm="HS256")

            return InlineResponse200(token=token), 200

        else:
            return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})
    else:
        return make_response('Invalid request format', 400)
