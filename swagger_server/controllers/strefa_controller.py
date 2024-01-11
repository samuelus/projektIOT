import connexion
import six

from swagger_server.models.inline_response2001 import InlineResponse2001  # noqa: E501
from swagger_server.models.inline_response2002 import InlineResponse2002  # noqa: E501
from swagger_server.models.inline_response201 import InlineResponse201  # noqa: E501
from swagger_server.models.strefa_body import StrefaBody  # noqa: E501
from swagger_server.models.strefa_id_body import StrefaIdBody  # noqa: E501
from swagger_server import util


def create_zone(body):  # noqa: E501
    """Create a new zone.

    This endpoint allows for the creation of a new zone by specifying its name. # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: InlineResponse201
    """
    if connexion.request.is_json:
        body = StrefaBody.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def delete_zone(id):  # noqa: E501
    """Delete a zone.

    This endpoint allows for the deletion of a zone by specifying its ID. # noqa: E501

    :param id: The unique identifier of the zone to be deleted.
    :type id: int

    :rtype: None
    """
    return 'do some magic!'


def edit_zone(body, id):  # noqa: E501
    """Edit a zone.

    This endpoint allows for the editing of a zone by specifying its ID and providing a new name. # noqa: E501

    :param body: 
    :type body: dict | bytes
    :param id: The unique identifier of the zone to be edited.
    :type id: int

    :rtype: None
    """
    if connexion.request.is_json:
        body = StrefaIdBody.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def get_zone_details(id):  # noqa: E501
    """Get details of a specific zone.

    This endpoint returns details of a specific zone including its ID, name, and a list of assigned employees. # noqa: E501

    :param id: The unique identifier of the zone.
    :type id: int

    :rtype: InlineResponse2002
    """
    return 'do some magic!'


def get_zones():  # noqa: E501
    """Get a list of all zones.

    This endpoint returns a list of all existing zones with their ID and name. # noqa: E501


    :rtype: List[InlineResponse2001]
    """
    return 'do some magic!'
