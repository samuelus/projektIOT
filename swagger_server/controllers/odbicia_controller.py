import connexion
import six

from swagger_server.models.inline_response2005 import InlineResponse2005  # noqa: E501
from swagger_server.models.inline_response400 import InlineResponse400  # noqa: E501
from swagger_server import util


def get_entries_exits_report(id_strefy=None, id_karty=None, czas_wejscia_od=None, czas_wejscia_do=None, czas_wyjscia_od=None, czas_wyjscia_do=None):  # noqa: E501
    """Get a report of entries and exits.

    This endpoint returns a report of card entries and exits to and from zones. The &#x60;czas_wejscia_od/do&#x60; and &#x60;czas_wyjscia_od/do&#x60; parameters should be in ISO 8601 format (YYYY-MM-DDTHH:MM:SSZ). The &#x60;czas_pobytu&#x60; is provided in seconds.  # noqa: E501

    :param id_strefy: Filter by zone ID.
    :type id_strefy: int
    :param id_karty: Filter by card ID.
    :type id_karty: int
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
    czas_wejscia_od = util.deserialize_datetime(czas_wejscia_od)
    czas_wejscia_do = util.deserialize_datetime(czas_wejscia_do)
    czas_wyjscia_od = util.deserialize_datetime(czas_wyjscia_od)
    czas_wyjscia_do = util.deserialize_datetime(czas_wyjscia_do)
    return 'do some magic!'
