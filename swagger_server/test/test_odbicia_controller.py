# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.inline_response2005 import InlineResponse2005  # noqa: E501
from swagger_server.models.inline_response400 import InlineResponse400  # noqa: E501
from swagger_server.test import BaseTestCase


class TestOdbiciaController(BaseTestCase):
    """OdbiciaController integration test stubs"""

    def test_get_entries_exits_report(self):
        """Test case for get_entries_exits_report

        Get a report of entries and exits.
        """
        query_string = [('id_strefy', 56),
                        ('id_karty', 56),
                        ('czas_wejscia_od', '2013-10-20T19:20:30+01:00'),
                        ('czas_wejscia_do', '2013-10-20T19:20:30+01:00'),
                        ('czas_wyjscia_od', '2013-10-20T19:20:30+01:00'),
                        ('czas_wyjscia_do', '2013-10-20T19:20:30+01:00')]
        response = self.client.open(
            '/odbicia',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
