#! /usr/bin/env python

import mosquitto
import time
import os
from datetime import datetime, timedelta
from random import choice

mqtt_client_id = "nerdctrl-luakit"
mqtt_server = "c-beam.cbrp3.c-base.org"
page_timeout = 300

urls = ["http://www.c-base.org", "http://logbuch.c-base.org/", "http://c-portal.c-base.org", 
    "http://c-beam.cbrp3.c-base.org/events", "https://c-beam.cbrp3.c-base.org/c-base-map",
    "http://cbag3.c-base.org/artefact", "https://c-beam.cbrp3.c-base.org/missions", "https://c-beam.cbrp3.c-base.org/weather",
    "http://c-beam.cbrp3.c-base.org/bvg", "http://c-beam.cbrp3.c-base.org/nerdctrl"]

last_change = datetime.now()

def mqtt_connect(client):
    try:
        client.connect(mqtt_server)
        client.subscribe("nerdctrl/+", 1)
        client.on_message = on_message
    except: pass

def mqtt_loop():
    global last_change
    client = mosquitto.Mosquitto(mqtt_client_id)
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
    if msg.topic == "nerdctrl/open":
        last_change = datetime.now()
        os.system('luakit %s' % msg.payload)

mqtt_loop()
