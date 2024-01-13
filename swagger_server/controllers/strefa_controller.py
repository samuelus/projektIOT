import connexion
import six

from swagger_server.controllers import pracownik_controller
from swagger_server.models.inline_response2001 import InlineResponse2001  # noqa: E501
from swagger_server.models.inline_response2002 import InlineResponse2002  # noqa: E501
from swagger_server.models.inline_response201 import InlineResponse201  # noqa: E501
from swagger_server.models.strefa_body import StrefaBody  # noqa: E501
from swagger_server.models.strefa_id_strefy_body import StrefaIdStrefyBody  # noqa: E501
from swagger_server import util
from database import db_manager

database = db_manager.DbManager
def create_zone(body):  # noqa: E501
    """Create a new zone.

    This endpoint allows for the creation of a new zone by specifying its name. # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: InlineResponse201
    """
    if connexion.request.is_json:
        body = StrefaBody.from_dict(connexion.request.get_json())
        if next((True for strefa in database.read_all_strefy() if strefa.nazwa == body.nazwa_strefy), False):
            return "Zone with provided name already exist", 409
        id_strefy = database.create_strefa(body.nazwa_strefy)
        return InlineResponse201(id=id_strefy, nazwa_strefy=body.nazwa_strefy), 201


def delete_zone(id_strefy):  # noqa: E501
    """Delete a zone.

    This endpoint allows for the deletion of a zone by specifying its ID. # noqa: E501

    :param id_strefy: The unique identifier of the zone to be deleted.
    :type id_strefy: int

    :rtype: None
    """
    success = database.delete_strefa(id_strefy)
    if success:
        return 'Zone deleted successfully', 200
    else:
        return 'No zone found with provided ID', 404


def edit_zone(body, id_strefy):  # noqa: E501
    """Edit a zone.

    This endpoint allows for the editing of a zone by specifying its ID and providing a new name. # noqa: E501

    :param body: 
    :type body: dict | bytes
    :param id_strefy: The unique identifier of the zone to be edited.
    :type id_strefy: int

    :rtype: None
    """
    if connexion.request.is_json:
        body = StrefaIdStrefyBody.from_dict(connexion.request.get_json())  # noqa: E501
        success = database.update_strefa(id_strefy, body.nazwa_strefy)
        if success:
            return 'Zone updated successfully', 200
        else:
            return 'No zone found with provided ID', 404


def get_zone_details(id_strefy):  # noqa: E501
    """Get details of a specific zone.

    This endpoint returns details of a specific zone including its ID, name, and a list of assigned employees. # noqa: E501

    :param id_strefy: The unique identifier of the zone.
    :type id_strefy: int

    :rtype: InlineResponse2002
    """
    strefa = database.read_strefa(id_strefy)
    if strefa:
        pracownicy_id = [filtered_uprawnienia.id_karty for filtered_uprawnienia in database.read_all_uprawnienia()
                                                       if filtered_uprawnienia.id_strefy == id_strefy]
        pracownicy = [filtered_pracownicy for filtered_pracownicy in database.read_all_pracownicy()
                                          if filtered_pracownicy.id_karty in pracownicy_id]
        pracownicy_dict = [pracownik_controller.pracownik_to_dict(pracownik) for pracownik in pracownicy]
        return InlineResponse2002(id=strefa.id_strefy, nazwa_strefy=strefa.nazwa, pracownicy=pracownicy_dict)
    else:
        return 'No zone found with provided ID', 404


def get_zones():  # noqa: E501
    """Get a list of all zones.

    This endpoint returns a list of all existing zones with their ID and name. # noqa: E501


    :rtype: List[InlineResponse2001]
    """
    strefy = database.read_all_strefy()
    strefy_dict = []
    for strefa in strefy:
        strefa_dict = {
            "id": strefa.id_strefy,
            "nazwaStrefy": strefa.nazwa
        }
        strefy_dict.append(strefa_dict)
    return [InlineResponse2001.from_dict(strefa_dict) for strefa_dict in strefy_dict]
