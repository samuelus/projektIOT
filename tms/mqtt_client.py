import paho.mqtt.client as mqtt
from datetime import datetime
import json
from constants import *
import traceback
import time


class MyMQTTClient:
    def __init__(self, on_get_response):
        self.client = mqtt.Client()
        self.client.connect(BROKER)
        print(f"Connection with broker {BROKER} established")
        self.client.on_message = self.on_message

        topic_to_subscribe = f"{MQTT_ODBICIA_STREFA_TOPIC}/{ID_STREFY}"
        self.client.subscribe(topic_to_subscribe)
        print(f"Client subscribed to topic {topic_to_subscribe}")
        self.client.loop_start()

        self.on_get_response = on_get_response

    def process_start_time(self, body):
        start_time = datetime.strptime(body['start_work_time'], '%Y-%m-%d %H:%M:%S')
        return f"Work start time saved: {start_time.strftime('%H:%M:%S')}"

    def process_work_duration(self, body):
        start_time = datetime.strptime(body['start_work_time'], '%Y-%m-%d %H:%M:%S')
        end_time = datetime.strptime(body['end_work_time'], '%Y-%m-%d %H:%M:%S')
        time_difference = end_time - start_time

        hours, remainder = divmod(time_difference.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"You worked for {hours} hours, {minutes} minutes, and {seconds} seconds."

    def on_message(self, client, userdata, msg):
        topic = msg.topic
        try:
            print(f"Received message from topic {topic}")
            m_decode = msg.payload.decode("utf-8", "ignore")
            print(m_decode)
            m_in = json.loads(m_decode)
            code = m_in['code']

            final_message = None

            if code == 'TMS-1005':
                final_message = self.process_start_time(json.loads(m_in['body']))

            elif code == 'TMS-1006':
                final_message = self.process_work_duration(json.loads(m_in['body']))
            else:
                final_message = messages[code]

            self.on_get_response(final_message)

        except Exception as e:
            traceback.print_exc()
            print(f"Something went wrong while processing event from {topic}")

    def odbicie(self, id_karty: str):
        data = {
            "id_karty": id_karty,
            "token_strefy": ID_STREFY,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        json_data = json.dumps(data)
        print("-" * 50)
        print(f"Sending: {json_data}")
        self.client.publish(MQTT_ODBICIA_TOPIC, json_data)


def on_get_response_callback(response):
    print(f"WILL BE DISPLAYED ---> || {response} ||")


if __name__ == "__main__":
    ID_KARTY = "h231yu8x21f3"

    my_mqtt_client = MyMQTTClient(on_get_response=on_get_response_callback)

    for i in range(10000):
        my_mqtt_client.odbicie(ID_KARTY)
        time.sleep(10)
