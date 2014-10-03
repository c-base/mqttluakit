#! /usr/bin/env python

import paho.mqtt.client as paho
import time
import os
import ssl
import json
from datetime import datetime, timedelta
from random import choice

from config import urls
from config import mqtt_client_id
from config import mqtt_client_name
from config import mqtt_client_password
import config 

mqtt_server = "c-beam.cbrp3.c-base.org"
page_timeout = 120

last_change = datetime.now()

def mqtt_connect(client):
    try:
        client.username_pw_set(mqtt_client_name, password=mqtt_client_password)
        if config.mqtt_server_tls:
            print client.tls_set(config.mqtt_server_cert, cert_reqs=ssl.CERT_OPTIONAL)
            print client.connect(mqtt_server, port=1884)
        else:
            print client.connect(mqtt_server)
        client.subscribe("+/+", 1)
        client.on_message = on_message
    except Exception as e: print(e)

def mqtt_loop():
    global last_change
    client = paho.Client(mqtt_client_id)
    mqtt_connect(client)
    while True:
        result = client.loop(1)
        if result != 0:
            mqtt_connect(client)
        time.sleep(0.5)
        if datetime.now() > last_change + timedelta(seconds=page_timeout):
            os.system("luakit %s" % choice(urls))
            last_change = datetime.now()

def on_message(m, obj, msg):
    global last_change
    if msg.topic == "%s/open" % mqtt_client_name:
        last_change = datetime.now()
        os.system('luakit %s' % msg.payload)
    if msg.topic == 'user/boarding':
        last_change = datetime.now()
        try:
            data = json.loads(msg.payload)
            os.system('luakit https://c-beam.cbrp3.c-base.org/welcome/%s' % data['user'])
        except:
            pass
    else:
        print msg.payload

mqtt_loop()
