from dotenv import load_dotenv
import os

load_dotenv()

messages = {
    "TMS-1001": "There is no registered card in the system",
    "TMS-1002": "There is no such strefa",
    "TMS-1003": "You don't have permission for this strefa",
    "TMS-1004": "You cannot exit in a different strefa",
    "TMS-1005": "Registered entrance",
    "TMS-1006": "Registered exit",
    "TMS-1007": "Something went wrong",
}

MQTT_ODBICIA_TOPIC = "/odbicia"
MQTT_ODBICIA_STREFA_TOPIC = "/odbicia/strefa"
BROKER = os.getenv('BROKER_ADDRESS') or 'localhost'
ID_STREFY = os.getenv('ID_STREFY') or 1