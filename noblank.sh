#! /bin/bash

export DISPLAY=:0.0
#xset dpms force on

xhost +localhost
xset dpms 0 0 0
xset dpms force on
xset s 0 0
xset s noblank
