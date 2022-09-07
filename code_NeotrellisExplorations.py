# SPDX-FileCopyrightText: 2021 Kattni Rembor for Adafruit Industries
# SPDX-License-Identifier: MIT

# 2022 07 16 preparing to refactor

"""
NeoTrellisExplorations: run CircuitPython aninmation library on neoTrellis
This is the main code intended to be code.py
other local files hold code for animations, keypad and midi
This code uses several libraries:
* the adafruit.neopixel library (for on-board single pixel)
* the adafruit_seesaw.neopixel for neotrellis comms
* adafruit_animation for color animation patterns
Animations and Keypad actions are in separate file for reuse
  neotrellis_animations: builds array of animations
  neotrellis_midi: handles midi sendOn/Off for key idx
  neotrelis_keypad: handles keypad and activates midi/animations
Runs a NeoTrellis with a Feather M4 processor. Other processors and more boards may come later
blinks all the pixels on startup
Then run a DefaultAnimation
When a key is pressed, any animation stops that key's led lights in keyColor[i]
When a key is released, it voids any existing animation and runs animations[i]
OnBoardNeopixel toggles on each press and each release
"""
# not sure why but mu editor/cp keeps doing a reload/soft reboot unless we do this
# so then we have to use Ctrl-D to reload with Mu editor
import supervisor
supervisor.disable_autoreload()
print("autoreload disabled")

import time
import board
import busio
from adafruit_neotrellis.neotrellis import NeoTrellis

# local modules
import onboard_neopixel
import neotrellis_animations
import neotrellis_keypad

# create the i2c object for the trellis
# note the use of busio.I2C() instead of board.I2C()
# apparently this is an issue for M4 (rPi Pico too?)
i2c_bus = busio.I2C(board.SCL, board.SDA)
trellis = NeoTrellis(i2c_bus)

# setup CPY single pixel strip if board has it, blink it once
onboard_neopixel.setup_onboard_neopixel()

# setup animation and keypad modules
neotrellis_animations.setup_animations(trellis)
neotrellis_keypad.setup_keypad(trellis)

print("Setup Complete enter forever loop ", neotrellis_animations.current_animation)

i = 0
while True:
    # tell animation to update
    neotrellis_animations.current_animation.animate()
    # call the sync function call any triggered callbacks
    trellis.sync()
    # the trellis can only be read every 17 milliseconds or so
    # really? the neopixel _getItem() could be an issue for i2c/seesaw connected neopixels
    time.sleep(0.02)
    # print out something so debug console watcher knows program is running
    # also might give keyboard interrupt (Ctrl C) a chance to pause CircuitPython
    i +=1
    if i%50 == 0:
        print(i, end='.')
    if i%10000 == 0:
        print(i, "reset")
        i=0
