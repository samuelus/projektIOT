import connexion
import six

from database import db_manager
from swagger_server.models.inline_response2003 import InlineResponse2003  # noqa: E501
from swagger_server.models.inline_response2004 import InlineResponse2004  # noqa: E501
from swagger_server.models.pracownik_body import PracownikBody  # noqa: E501
from swagger_server.models.pracownik_id_karty_body import PracownikIdKartyBody  # noqa: E501
from swagger_server import util

database = db_manager.DbManager

def pracownik_to_dict(pracownik):
    pracownik_dict = {
        "id": pracownik.id_karty,
        "imie": pracownik.imie,
        "nazwisko": pracownik.nazwisko
    }
    return pracownik_dict

def add_employee(body):  # noqa: E501
    """Add a new employee.

    This endpoint allows for adding a new employee with their name, surname, and a list of zone IDs they have access to. # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = PracownikBody.from_dict(connexion.request.get_json())  # noqa: E501
        success = database.create_pracownik(body.id, body.imie, body.nazwisko)
        if success:
            success = []
            for strefa_dostepu in body.strefy_dostepu:
                success.append(database.create_uprawnienia(body.id, strefa_dostepu))
            if all(success):
                return 'Employee added successfully', 201
            else:
                database.delete_pracownik(body.id)
                return 'Internal error', 500
        else:
            return 'Employee with provided ID already exists', 409


def delete_employee(id_karty):  # noqa: E501
    """Delete an employee.

    This endpoint allows for the deletion of an employee by specifying their ID. # noqa: E501

    :param id_karty: The unique identifier of the employee to be deleted.
    :type id_karty: str

    :rtype: None
    """
    success = database.delete_pracownik(id_karty)
    uprawnienia = [filtered_uprawnienia.id_strefy for filtered_uprawnienia in database.read_all_uprawnienia()
                                                  if filtered_uprawnienia.id_karty == id_karty]
    for uprawnienie in uprawnienia:
        database.delete_uprawnienia(id_karty, uprawnienie)
    if success:
        return 'Employee deleted successfully', 200
    else:
        return 'No employee found with provided ID', 404


def edit_employee(body, id_karty):  # noqa: E501
    """Edit an employee&#x27;s details.

    This endpoint allows for editing an employee&#x27;s name, surname, and the list of accessible zones by specifying their ID. # noqa: E501

    :param body: 
    :type body: dict | bytes
    :param id_karty: The unique identifier of the employee to be edited.
    :type id_karty: str

    :rtype: None
    """
    if connexion.request.is_json:
        body = PracownikIdKartyBody.from_dict(connexion.request.get_json())  # noqa: E501
        success = database.update_pracownik(id_karty, body.imie, body.nazwisko)
        if success:
            uprawnienia = [filtered_uprawnienia.id_strefy for filtered_uprawnienia in database.read_all_uprawnienia()
                                            if filtered_uprawnienia.id_karty == id_karty]
            for strefa_dostepu in body.strefy_dostepu:
                if strefa_dostepu not in uprawnienia:
                    database.create_uprawnienia(id_karty, strefa_dostepu)
            for uprawnienie in uprawnienia:
                if uprawnienie not in body.strefy_dostepu:
                    database.delete_uprawnienia(id_karty, uprawnienie)
            return 'Employee updated successfully', 200
        else:
            return 'No employee found with provided ID', 404


def get_all_employees():  # noqa: E501
    """Get a list of all employees.

    This endpoint returns a list of all employees, including their first name, last name, and ID. # noqa: E501


    :rtype: List[InlineResponse2003]
    """
    pracownicy = database.read_all_pracownicy()
    return [InlineResponse2003.from_dict(pracownik_to_dict(pracownik)) for pracownik in pracownicy]


def get_employee_details(id_karty):  # noqa: E501
    """Get an employee&#x27;s details.

    This endpoint returns detailed information about an employee, including their name, surname, ID, and the list of accessible zones. # noqa: E501

    :param id_karty: The unique identifier of the employee.
    :type id_karty: str

    :rtype: InlineResponse2004
    """
    pracownik = database.read_pracownik(id_karty)
    if pracownik:
        pracownik_dict = pracownik_to_dict(pracownik)
        pracownik_dict["strefyDostepu"] = \
            [filtered_uprawnienia.id_strefy for filtered_uprawnienia in database.read_all_uprawnienia()
                                            if filtered_uprawnienia.id_karty == id_karty]
        return InlineResponse2004(id=pracownik_dict['id'],
                                  imie=pracownik_dict['imie'],
                                  nazwisko=pracownik_dict['nazwisko'],
                                  strefy_dostepu=pracownik_dict["strefyDostepu"])
    else:
        return 'No employee found with provided ID', 404
