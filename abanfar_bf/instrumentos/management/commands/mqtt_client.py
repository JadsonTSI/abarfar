import json
from django.core.management.base import BaseCommand
from django.db import transaction
from instrumentos.models import IoTScan, Instrumento
import paho.mqtt.client as mqtt

# Configurações do Broker MQTT
MQTT_BROKER = "broker.hivemq.com"
MQTT_PORT = 1883
MQTT_TOPIC = "abanfar/iot/scan"

class Command(BaseCommand):
    help = "Inicia o cliente MQTT para escutar leituras do leitor RFID IoT (ESP32)"

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS(f"Iniciando cliente MQTT conectando a {MQTT_BROKER}:{MQTT_PORT}..."))
        
        # paho-mqtt v2.0+ exige informar a versão da API de callback
        client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2)
        client.on_connect = self.on_connect
        client.on_message = self.on_message
        
        try:
            client.connect(MQTT_BROKER, MQTT_PORT, 60)
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Falha ao conectar ao broker: {e}"))
            return

        # Loop em segundo plano para escutar mensagens continuamente
        try:
            self.stdout.write("Pressione Ctrl+C para encerrar o cliente.")
            client.loop_forever()
        except KeyboardInterrupt:
            self.stdout.write(self.style.WARNING("\nParando cliente MQTT..."))

    def on_connect(self, client, userdata, flags, reason_code, properties):
        if reason_code == 0:
            self.stdout.write(self.style.SUCCESS(f"Conectado com sucesso! Se inscrevendo no tópico: '{MQTT_TOPIC}'"))
            client.subscribe(MQTT_TOPIC)
        else:
            self.stdout.write(self.style.ERROR(f"Falha na conexão. Código de retorno: {reason_code}"))

    def on_message(self, client, userdata, msg):
        try:
            payload = msg.payload.decode('utf-8')
            self.stdout.write(f"Mensagem recebida no tópico {msg.topic}: {payload}")
            
            # Tentar decodificar JSON, se falhar assume que é a tag RFID pura
            try:
                data = json.loads(payload)
                rfid = data.get('rfid')
            except json.JSONDecodeError:
                rfid = payload
            
            if not rfid:
                self.stdout.write(self.style.WARNING("RFID não encontrado na mensagem."))
                return
                
            rfid = rfid.strip()
            
            # Salvar no banco de forma atômica
            with transaction.atomic():
                scan = IoTScan.objects.create(rfid=rfid)
                
                # Manter apenas as últimas 50 leituras no banco
                total_scans = IoTScan.objects.count()
                if total_scans > 50:
                    old_scans = IoTScan.objects.order_by('id')[:total_scans - 50]
                    for old in old_scans:
                        old.delete()
                        
            inst = Instrumento.objects.filter(rfid=rfid).first()
            if inst:
                self.stdout.write(self.style.SUCCESS(f"Leitura gravada: Tag '{rfid}' (Vinculada ao instrumento: {inst.nome})"))
            else:
                self.stdout.write(self.style.SUCCESS(f"Leitura gravada: Tag '{rfid}' (Tag não vinculada)"))
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Erro ao processar mensagem MQTT: {e}"))
