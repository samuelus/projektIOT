from flask import make_response

from swagger_server import util
from swagger_server.models.inline_response2005 import InlineResponse2005  # noqa: E501

from database import db_manager
from datetime import datetime

import connexion
import six

from swagger_server.models.average_work_time_body import AverageWorkTimeBody  # noqa: E501
from swagger_server.models.inline_response2005 import InlineResponse2005  # noqa: E501
from swagger_server.models.inline_response400 import InlineResponse400  # noqa: E501
from swagger_server.models.total_work_time_body import TotalWorkTimeBody  # noqa: E501
from swagger_server.models.total_work_unit_body import TotalWorkUnitBody  # noqa: E501
from swagger_server import util


def average_work_time(start_date, end_date):  # noqa: E501
    """Get average work time of each employee between dates.

    This endpoint returns the average work time for each employee between the given start and end dates.  # noqa: E501

    :param start_date: The start date in ISO 8601 format.
    :type start_date: str
    :param end_date: The end date in ISO 8601 format.
    :type end_date: str

    :rtype: List[AverageWorkTimeBody]
    """
    start_date = util.deserialize_datetime(start_date)
    end_date = util.deserialize_datetime(end_date)
    return 'do some magic!'


def get_entries_exits_report(id_strefy=None, id_karty=None, czas_wejscia_od=None, czas_wejscia_do=None,
                             czas_wyjscia_od=None, czas_wyjscia_do=None):  # noqa: E501
    """Get a report of entries and exits.

    This endpoint returns a report of card entries and exits to and from zones. The &#x60;czas_wejscia_od/do&#x60; and &#x60;czas_wyjscia_od/do&#x60; parameters should be in ISO 8601 format (YYYY-MM-DDTHH:MM:SSZ). The &#x60;czas_pobytu&#x60; is provided in seconds.  # noqa: E501

    :param id_strefy: Filter by zone ID.
    :type id_strefy: int
    :param id_karty: Filter by card ID.
    :type id_karty: str
    :param czas_wejscia_od: Filter entries from this datetime in ISO 8601 format.
    :type czas_wejscia_od: str
    :param czas_wejscia_do: Filter entries until this datetime in ISO 8601 format.
    :type czas_wejscia_do: str
    :param czas_wyjscia_od: Filter exits from this datetime in ISO 8601 format.
    :type czas_wyjscia_od: str
    :param czas_wyjscia_do: Filter exits until this datetime in ISO 8601 format.
    :type czas_wyjscia_do: str

    :rtype: List[InlineResponse2005]
    """
    try:
        if czas_wejscia_od:
            czas_wejscia_od = util.deserialize_datetime(czas_wejscia_od).replace(tzinfo=None)
        if czas_wejscia_do:
            czas_wejscia_do = util.deserialize_datetime(czas_wejscia_do).replace(tzinfo=None)
        if czas_wyjscia_od:
            czas_wyjscia_od = util.deserialize_datetime(czas_wyjscia_od).replace(tzinfo=None)
        if czas_wyjscia_do:
            czas_wyjscia_do = util.deserialize_datetime(czas_wyjscia_do).replace(tzinfo=None)
    except ValueError as e:
        return make_response(str(e), 400)
    database = db_manager.DbManager
    odbicia = database.read_all_odbicia()
    strefy_dict = {strefa.id_strefy: strefa.nazwa for strefa in database.read_all_strefy()}
    if id_strefy:
        odbicia = filter(lambda filtered_odbicia: filtered_odbicia.id_strefy == id_strefy, odbicia)
    if id_karty:
        odbicia = filter(lambda filtered_odbicia: filtered_odbicia.id_karty == id_karty, odbicia)
    if czas_wejscia_od:
        odbicia = filter(lambda filtered_odbicia: filtered_odbicia.czas_wejscia >= czas_wejscia_od, odbicia)
    if czas_wejscia_do:
        odbicia = filter(lambda filtered_odbicia: filtered_odbicia.czas_wejscia <= czas_wejscia_do, odbicia)
    if czas_wyjscia_od:
        odbicia = filter(lambda filtered_odbicia: filtered_odbicia.czas_wejscia >= czas_wyjscia_od, odbicia)
    if czas_wyjscia_do:
        odbicia = filter(lambda filtered_odbicia: filtered_odbicia.czas_wejscia <= czas_wyjscia_do, odbicia)
    odbicia_dict = [{
        **odbicie.to_dict(),
        "nazwa_strefy": strefy_dict.get(odbicie.id_strefy),
        "czas_pobytu": (odbicie.czas_wyjscia - odbicie.czas_wejscia).total_seconds()
        if odbicie.czas_wyjscia and odbicie.czas_wejscia else None
    } for odbicie in odbicia]
    return [InlineResponse2005.from_dict(item) for item in odbicia_dict]


def total_work_time(start_date, end_date):  # noqa: E501
    """Get total work time of each employee between dates.

    This endpoint returns the total work time for each employee between the given start and end dates. The &#x60;calkowity_czas_pracy&#x60; is provided in seconds.  # noqa: E501

    :param start_date: The start date in ISO 8601 format.
    :type start_date: str
    :param end_date: The end date in ISO 8601 format.
    :type end_date: str

    :rtype: List[TotalWorkTimeBody]
    """
    start_date = util.deserialize_datetime(start_date)
    end_date = util.deserialize_datetime(end_date)
    return 'do some magic!'


def total_work_unit(start_date, end_date):  # noqa: E501
    """Get total work unit of each employee between dates.

    This endpoint returns the total work unit for each employee between the given start and end dates.  # noqa: E501

    :param start_date: The start date in ISO 8601 format.
    :type start_date: str
    :param end_date: The end date in ISO 8601 format.
    :type end_date: str

    :rtype: List[TotalWorkUnitBody]
    """
    start_date = util.deserialize_datetime(start_date)
    end_date = util.deserialize_datetime(end_date)
    return 'do some magic!'
