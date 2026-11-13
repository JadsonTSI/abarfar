import sys
import json
import random
import paho.mqtt.client as mqtt

# Configurações do Broker MQTT
MQTT_BROKER = "broker.hivemq.com"
MQTT_PORT = 1883
MQTT_TOPIC = "abanfar/iot/scan"

# Lista de tags RFID simuladas para teste
TAGS_TESTE = [
    "12A34B56C7",  # Trompete
    "98D76C54B3",  # Saxofone
    "45E67F89A0",  # Clarinete
    "E1F2A3B4C5",  # Tag Nova (Não vinculada)
    "90A1B2C3D4",  # Tag Nova (Não vinculada)
]

def main():
    # paho-mqtt v2.0+ exige informar a versão da API de callback
    client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2)
    
    try:
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
    except Exception as e:
        print(f"Erro ao conectar ao broker: {e}")
        sys.exit(1)
        
    client.loop_start()
    
    # Determinar a tag a ser publicada
    if len(sys.argv) > 1:
        rfid = sys.argv[1]
    else:
        rfid = random.choice(TAGS_TESTE)
        
    payload = json.dumps({"rfid": rfid})
    
    print(f"Conectado ao broker MQTT '{MQTT_BROKER}'")
    print(f"Publicando leitura no tópico '{MQTT_TOPIC}'...")
    print(f"Payload: {payload}")
    
    info = client.publish(MQTT_TOPIC, payload, qos=1)
    info.wait_for_publish()
    
    print("Mensagem publicada com sucesso!")
    
    client.loop_stop()
    client.disconnect()

if __name__ == "__main__":
    main()
