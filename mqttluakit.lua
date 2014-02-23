#!/usr/bin/lua

function callback(
  topic,    -- string
  message)  -- string

  print("Topic: " .. topic .. ", message: '" .. message .. "'")
  
  os.execute("luakit " ..  message)
end

function mqtt_loop()
  print("[mqtt_subscribe v0.2 2012-06-01]")

  local MQTT = require("mqtt_library")

  MQTT.Utility.set_debug(false)
  MQTT.client.KEEP_ALIVE_TIME = 60

  local mqtt_client = MQTT.client.create("c-beam.cbrp3.c-base.org", 1883, callback)

  mqtt_client:connect("nerdctrl-browser")
  mqtt_client:subscribe({"nerdctrl/open"})

  local error_message = nil

  while (error_message == nil) do
    error_message = mqtt_client:handler()
    socket.sleep(1.0)  -- seconds
  end

  if (error_message == nil) then
    mqtt_client:unsubscribe("nerdctrl/open")
    mqtt_client:destroy()
  else
    print(error_message)
  end
end

--co = coroutine.create(mqtt_loop)
--coroutine.resume(co)
mqtt_loop()

-- ------------------------------------------------------------------------- --





-- vim: et:sw=4:ts=8:sts=4:tw=80
