# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.average_work_time_body import AverageWorkTimeBody  # noqa: E501
from swagger_server.models.inline_response2005 import InlineResponse2005  # noqa: E501
from swagger_server.models.inline_response400 import InlineResponse400  # noqa: E501
from swagger_server.models.total_work_time_body import TotalWorkTimeBody  # noqa: E501
from swagger_server.models.total_work_unit_body import TotalWorkUnitBody  # noqa: E501
from swagger_server.test import BaseTestCase


class TestOdbiciaController(BaseTestCase):
    """OdbiciaController integration test stubs"""

    def test_average_work_time(self):
        """Test case for average_work_time

        Get average work time of each employee between dates.
        """
        query_string = [('start_date', '2013-10-20T19:20:30+01:00'),
                        ('end_date', '2013-10-20T19:20:30+01:00')]
        response = self.client.open(
            '/api/odbicia/average-work-time',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_entries_exits_report(self):
        """Test case for get_entries_exits_report

        Get a report of entries and exits.
        """
        query_string = [('id_strefy', 56),
                        ('id_karty', 'id_karty_example'),
                        ('czas_wejscia_od', '2013-10-20T19:20:30+01:00'),
                        ('czas_wejscia_do', '2013-10-20T19:20:30+01:00'),
                        ('czas_wyjscia_od', '2013-10-20T19:20:30+01:00'),
                        ('czas_wyjscia_do', '2013-10-20T19:20:30+01:00')]
        response = self.client.open(
            '/api/odbicia',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_total_work_time(self):
        """Test case for total_work_time

        Get total work time of each employee between dates.
        """
        query_string = [('start_date', '2013-10-20T19:20:30+01:00'),
                        ('end_date', '2013-10-20T19:20:30+01:00')]
        response = self.client.open(
            '/api/odbicia/total-work-time',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_total_work_unit(self):
        """Test case for total_work_unit

        Get total work unit of each employee between dates.
        """
        query_string = [('start_date', '2013-10-20T19:20:30+01:00'),
                        ('end_date', '2013-10-20T19:20:30+01:00')]
        response = self.client.open(
            '/api/odbicia/total-work-unit',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
