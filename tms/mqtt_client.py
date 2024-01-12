import paho.mqtt.client as mqtt
from datetime import datetime
import json
from constants import *
import traceback


def process_start_time(body):
    start_time = datetime.strptime(body['start_work_time'], '%Y-%m-%d %H:%M:%S')
    print(f"Work start time saved: {start_time.strftime('%H:%M:%S')}")


def process_work_duration(body):
    start_time = datetime.strptime(body['start_work_time'], '%Y-%m-%d %H:%M:%S')
    end_time = datetime.strptime(body['end_work_time'], '%Y-%m-%d %H:%M:%S')
    time_difference = end_time - start_time

    hours, remainder = divmod(time_difference.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    print(f"You worked for {hours} hours, {minutes} minutes, and {seconds} seconds.")


def on_message(client, userdata, msg):
    topic = msg.topic
    try:
        print(f"Received message from topic {topic}")
        m_decode = msg.payload.decode("utf-8", "ignore")
        print(m_decode)
        m_in = json.loads(m_decode)
        code = m_in['code']

        if code == 'TMS-1005':
            process_start_time(json.loads(m_in['body']))

        elif code == 'TMS-1006':
            process_work_duration(json.loads(m_in['body']))

        else:
            print(messages[code])

    except Exception as e:
        traceback.print_exc()
        print(f"Something went wrong while processing event from {topic}")

STREFA_ID = 1

client = mqtt.Client()
client.connect(BROKER)
print(f"Connection with broker {BROKER} established")
client.on_message = on_message

topic_to_subscribe = f"{MQTT_ODBICIA_STREFA_TOPIC}/{STREFA_ID}"

client.subscribe(topic_to_subscribe)
print(f"Client subscribed to topic {topic_to_subscribe}")
client.loop_start()

def odbicie(id_karty: str):
    data = {
        "id_karty": id_karty,
        "token_strefy": STREFA_ID,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    json_data = json.dumps(data)
    print("-" * 50)
    print(f"Sending: {json_data}")
    client.publish(MQTT_ODBICIA_TOPIC, json_data)
