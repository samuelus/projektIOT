import connexion
import six

from swagger_server.models.admin_login_body import AdminLoginBody  # noqa: E501
from swagger_server.models.inline_response200 import InlineResponse200  # noqa: E501
from swagger_server import util


def login_admin(body):  # noqa: E501
    """Log in to the system.

    This endpoint authenticates users and provides a JWT token for accessing secure endpoints. # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: InlineResponse200
    """
    if connexion.request.is_json:
        body = AdminLoginBody.from_dict(connexion.request.get_json())  # noqa: E501

    return 'do some magic!'
