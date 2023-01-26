# MQTT мост для Ирины
# Автор: Alexander Degtyarev © 2023, MIT
# https://github.com/aadegtyarev/irene-voice-assistant-mqtt-plugin

import os
import random
import paho.mqtt.client as mqtt
import codecs
import json

from vacore import VACore

modname = os.path.basename(__file__)[:-3]

# функция на старте
def start(core:VACore):
    manifest = {
        "name": "MQTT мост",
        "version": "0.1",
        "require_online": True,

        "default_options": {
            "mqtt_broker": "192.168.2.108",
            "mqtt_port": 1883,
            "mqtt_user": "",
            "mqtt_password": "",
            "mqtt_topic": "irine-voice-assistant"
        },
        # команды-триггеры, которые запускают нужные вам функции
        "commands": {
            "включи": mqtt_switch_on,
            "выключи": mqtt_switch_off,
        }
    }
    global global_core; global_core = core
    mqtt_connect(manifest["default_options"])
    return manifest

def start_with_options(core:VACore, manifest:dict):
    pass

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    return

def on_message(client, userdata, msg):
    if (len(msg.payload)>0):
        data = json.loads(msg.payload)
        global_core.play_voice_assistant_speech(data["phrase"])
    return

def mqtt_connect(options:dict):
    client_id = f'python-mqtt-{random.randint(0, 1000)}'
    global client; client = mqtt.Client(client_id)
    client.on_connect = on_connect
    client.on_message = on_message
    client.username_pw_set(options['mqtt_user'], options['mqtt_password'])
    client.connect(options['mqtt_broker'], options['mqtt_port'], 60)
    client.loop_start()
    client.subscribe(options['mqtt_topic']+"/say")
    return client

# универсальная функция отправки команд в MQTT
def mqtt_send_command(core:VACore, device:str, action):
    try:
        options = core.plugin_options(modname)
        client.publish(options['mqtt_topic']+"/command", json.dumps({"device":device, "action": action}))
    except:
        import traceback
        traceback.print_exc()
        core.play_voice_assistant_speech("Не получилось отправить команду устройству")
        return

# колбек функции, описанные в manifest["commands"]
def mqtt_switch_on(core:VACore, phrase:str):
    mqtt_send_command(core, phrase, "ON")

def mqtt_switch_off(core:VACore, phrase:str):
    mqtt_send_command(core, phrase, "OFF")
