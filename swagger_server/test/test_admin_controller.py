# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.admin_login_body import AdminLoginBody  # noqa: E501
from swagger_server.models.inline_response200 import InlineResponse200  # noqa: E501
from swagger_server.test import BaseTestCase


class TestAdminController(BaseTestCase):
    """AdminController integration test stubs"""

    def test_login_admin(self):
        """Test case for login_admin

        Log in to the system.
        """
        body = AdminLoginBody()
        response = self.client.open(
            '/api/admin/login',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
