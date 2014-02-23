#! /bin/bash

# kill all existing luakit instances and start a luakit instances waiting for mqtt calls

killall luakit
export DISPLAY=:0.0
/usr/bin/luakit --display=:0.0 http://c-beam.cbrp3.c-base.org/nerdctrl & 
sleep 5
