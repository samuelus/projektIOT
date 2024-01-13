# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.inline_response2003 import InlineResponse2003  # noqa: E501
from swagger_server.models.inline_response2004 import InlineResponse2004  # noqa: E501
from swagger_server.models.pracownik_body import PracownikBody  # noqa: E501
from swagger_server.models.pracownik_id_karty_body import PracownikIdKartyBody  # noqa: E501
from swagger_server.test import BaseTestCase


class TestPracownikController(BaseTestCase):
    """PracownikController integration test stubs"""

    def test_add_employee(self):
        """Test case for add_employee

        Add a new employee.
        """
        body = PracownikBody()
        response = self.client.open(
            '/pracownik',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_delete_employee(self):
        """Test case for delete_employee

        Delete an employee.
        """
        response = self.client.open(
            '/pracownik/{id_karty}'.format(id_karty='id_karty_example'),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_edit_employee(self):
        """Test case for edit_employee

        Edit an employee's details.
        """
        body = PracownikIdKartyBody()
        response = self.client.open(
            '/pracownik/{id_karty}'.format(id_karty='id_karty_example'),
            method='PUT',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_all_employees(self):
        """Test case for get_all_employees

        Get a list of all employees.
        """
        response = self.client.open(
            '/pracownicy',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_employee_details(self):
        """Test case for get_employee_details

        Get an employee's details.
        """
        response = self.client.open(
            '/pracownik/{id_karty}'.format(id_karty='id_karty_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
