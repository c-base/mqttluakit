#! /usr/bin/env python

import mosquitto
import time
import os
from datetime import datetime, timedelta
from random import choice

from config import urls
from config import mqtt_client_id
from config import mqtt_client_name

mqtt_server = "c-beam.cbrp3.c-base.org"
page_timeout = 120


#urls = ["http://www.c-base.org", "http://logbuch.c-base.org/", "http://c-portal.c-base.org", 
    #"http://c-beam.cbrp3.c-base.org/events", "https://c-beam.cbrp3.c-base.org/c-base-map",
    #"http://cbag3.c-base.org/artefact", "https://c-beam.cbrp3.c-base.org/missions", "https://c-beam.cbrp3.c-base.org/weather",
    #"http://c-beam.cbrp3.c-base.org/bvg", "http://c-beam.cbrp3.c-base.org/nerdctrl",
    #"https://c-beam.cbrp3.c-base.org/rickshaw/examples/fixed.html",
    #"https://c-beam.cbrp3.c-base.org/sensors",
    #"https://c-beam.cbrp3.c-base.org/ceitloch",
    #"http://visibletweets.com/#query=@cbase&animation=2",
    #"https://c-beam.cbrp3.c-base.org/reddit",
    #"http://vimeo.com/cbase/videos",
    #"https://wiki.cbrp3.c-base.org/dokuwiki/",
#]

last_change = datetime.now()

def mqtt_connect(client):
    try:
        client.connect(mqtt_server)
        client.subscribe("+/+", 1)
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
    if msg.topic == "%s/open" % mqtt_client_name:
        last_change = datetime.now()
        os.system('luakit %s' % msg.payload)
    if msg.topic == 'user/boarding':
        last_change = datetime.now()
        os.system('luakit https://c-beam.cbrp3.c-base.org/welcome/%s' % msg.payload)
        
    else:
        print msg.payload
   

mqtt_loop()
