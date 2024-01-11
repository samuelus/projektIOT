import connexion
import six

from swagger_server.models.inline_response2003 import InlineResponse2003  # noqa: E501
from swagger_server.models.inline_response2004 import InlineResponse2004  # noqa: E501
from swagger_server.models.pracownik_body import PracownikBody  # noqa: E501
from swagger_server.models.pracownik_id_body import PracownikIdBody  # noqa: E501
from swagger_server import util


def add_employee(body):  # noqa: E501
    """Add a new employee.

    This endpoint allows for adding a new employee with their name, surname, and a list of zone IDs they have access to. # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = PracownikBody.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def delete_employee(id):  # noqa: E501
    """Delete an employee.

    This endpoint allows for the deletion of an employee by specifying their ID. # noqa: E501

    :param id: The unique identifier of the employee to be deleted.
    :type id: int

    :rtype: None
    """
    return 'do some magic!'


def edit_employee(body, id):  # noqa: E501
    """Edit an employee&#x27;s details.

    This endpoint allows for editing an employee&#x27;s name, surname, and the list of accessible zones by specifying their ID. # noqa: E501

    :param body: 
    :type body: dict | bytes
    :param id: The unique identifier of the employee to be edited.
    :type id: int

    :rtype: None
    """
    if connexion.request.is_json:
        body = PracownikIdBody.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def get_all_employees():  # noqa: E501
    """Get a list of all employees.

    This endpoint returns a list of all employees, including their first name, last name, and ID. # noqa: E501


    :rtype: List[InlineResponse2003]
    """
    return 'do some magic!'


def get_employee_details(id):  # noqa: E501
    """Get an employee&#x27;s details.

    This endpoint returns detailed information about an employee, including their name, surname, ID, and the list of accessible zones. # noqa: E501

    :param id: The unique identifier of the employee.
    :type id: int

    :rtype: InlineResponse2004
    """
    return 'do some magic!'
