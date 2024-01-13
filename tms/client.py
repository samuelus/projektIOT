from mqtt_client import odbicie
import time

ID_KARTY = "h231yu8x21f3"
if __name__ == "__main__":
    for i in range(10000):
        odbicie(ID_KARTY)
        time.sleep(10)