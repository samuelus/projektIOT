import paho.mqtt.client as mqtt
import json
from database import db_manager
from datetime import datetime
from constants import *


def process_request(card_id: str, strefa_id: int, time: datetime):
    # Check if the employee exists
    pracownik = db_manager.DbManager.read_pracownik(card_id)
    if pracownik is None:
        return handle_error('TMS-1001')

    # Check if the zone exists
    strefa = db_manager.DbManager.read_strefa(strefa_id)
    if strefa is None:
        return handle_error('TMS-1002')

    # Check if the card has permissions for the specified zone
    uprawnienia = db_manager.DbManager.read_uprawnienia_by_id_karty(card_id)
    if strefa_id not in uprawnienia:
        return handle_error('TMS-1003')

    # Check the last entrance record for the card
    last_odbicie = db_manager.DbManager.read_last_entrance_by_card_id(card_id)

    # Process entrance or exit based on the last entrance record
    if not last_odbicie or last_odbicie.czas_wyjscia is not None:
        return process_entrance(card_id, strefa_id, time)
    else:
        return process_exit(card_id, strefa_id, time, last_odbicie)


def process_entrance(card_id, strefa_id, time):
    new_id = db_manager.DbManager.create_odbicie(card_id, strefa_id, time, None)
    print(f"Registered entrance({new_id}) with card_id {card_id} and strefa_id {strefa_id}: {time}")

    code = 'TMS-1005'
    body = {"start_work_time": time.strftime('%Y-%m-%d %H:%M:%S')}
    return create_response(code, body)


def process_exit(card_id, strefa_id, time, last_odbicie):
    if strefa_id != last_odbicie.id_strefy:
        return handle_error('TMS-1004')

    print(f"Registered exit ({last_odbicie.id_odbicia}) with card_id {card_id} and strefa_id {strefa_id}: {time}")
    db_manager.DbManager.update_odbicie(
        last_odbicie.id_odbicia,
        card_id,
        strefa_id,
        last_odbicie.czas_wejscia,
        time
    )

    code = 'TMS-1006'
    body = {
        "start_work_time": last_odbicie.czas_wejscia.strftime('%Y-%m-%d %H:%M:%S'),
        "end_work_time": time.strftime('%Y-%m-%d %H:%M:%S')
    }
    return create_response(code, body)


def handle_error(error_code):
    print(messages[error_code])
    return {"code": error_code}


def create_response(code, body=None):
    response = {"code": code}
    if body:
        response["body"] = json.dumps(body)
    return response


def on_message(client, userdata, msg):
    topic = msg.topic
    response = None
    try:
        m_decode = str(msg.payload.decode("utf-8", "ignore"))
        print(f"{topic} | Data Received: {m_decode}")
        m_in = json.loads(m_decode)
        czas = datetime.strptime(m_in['timestamp'], '%Y-%m-%d %H:%M:%S')
        id_karty = m_in['id_karty']
        strefa = int(m_in['token_strefy'])

        response = process_request(id_karty, strefa, czas)
        topic_to_publish = MQTT_ODBICIA_STREFA_TOPIC + "/" + str(strefa)
        print("Publishing to topic: " + topic_to_publish)
        client.publish(topic_to_publish, json.dumps(response))
    except Exception as e:
        print(f"Something went wrong while processing event from {topic}")


if __name__ == "__main__":
    db_manager.DbManager.clear_database(True)
    client = mqtt.Client()
    client.connect(BROKER)
    print(f"Connection with broker {BROKER} established")
    client.on_message = on_message
    client.subscribe(MQTT_ODBICIA_TOPIC)
    client.loop_forever()