by zezwolić na nieautoryzowany dostęp zdalny do brokera na Raspberry Pi należy w pliku
/etc/mosquitto/mosquitto.conf dopisać następujące linie:
allow_anonymous true
listener 1883 0.0.0.0

sudo systemctl start mosquitto.service
