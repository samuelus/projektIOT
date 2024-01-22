# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.inline_response2001 import InlineResponse2001  # noqa: E501
from swagger_server.models.inline_response2002 import InlineResponse2002  # noqa: E501
from swagger_server.models.inline_response201 import InlineResponse201  # noqa: E501
from swagger_server.models.strefa_body import StrefaBody  # noqa: E501
from swagger_server.models.strefa_id_strefy_body import StrefaIdStrefyBody  # noqa: E501
from swagger_server.test import BaseTestCase


class TestStrefaController(BaseTestCase):
    """StrefaController integration test stubs"""

    def test_create_zone(self):
        """Test case for create_zone

        Create a new zone.
        """
        body = StrefaBody()
        response = self.client.open(
            '/api/strefa',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_delete_zone(self):
        """Test case for delete_zone

        Delete a zone.
        """
        response = self.client.open(
            '/api/strefa/{id_strefy}'.format(id_strefy=789),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_edit_zone(self):
        """Test case for edit_zone

        Edit a zone.
        """
        body = StrefaIdStrefyBody()
        response = self.client.open(
            '/api/strefa/{id_strefy}'.format(id_strefy=789),
            method='PUT',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_zone_details(self):
        """Test case for get_zone_details

        Get details of a specific zone.
        """
        response = self.client.open(
            '/api/strefa/{id_strefy}'.format(id_strefy=789),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_zones(self):
        """Test case for get_zones

        Get a list of all zones.
        """
        response = self.client.open(
            '/api/strefy',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
