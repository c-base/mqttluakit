#! /usr/bin/env python

import paho.mqtt.client as paho
import time
import os
import ssl
from datetime import datetime, timedelta
from random import choice

from config import urls
from config import mqtt_client_id
from config import mqtt_client_name
from config import mqtt_client_password
import config 

from selenium import webdriver

#fp = webdriver.FirefoxProfile()
#fp.add_extension("r_kiosk-0.9.0-fx.xpi")
#driver = webdriver.Firefox(firefox_profile=fp)
options = webdriver.ChromeOptions()
options.add_argument('--kiosk')
options.add_argument('--test-type')
options.add_argument('--disable-web-security')
driver = webdriver.Chrome(chrome_options=options);
driver.get("https://c-beam.cbrp3.c-base.org/bar/calc")


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
            driver.get(choice(urls))
            #os.system("luakit %s" % choice(urls))
            last_change = datetime.now()

def on_message(m, obj, msg):
    global last_change
    if msg.topic == "%s/open" % mqtt_client_name:
        last_change = datetime.now()
        #os.system('luakit %s' % msg.payload)
        driver.get(msg.payload)
    else:
        print msg.payload

mqtt_loop()
