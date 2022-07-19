# SPDX-FileCopyrightText: 2021 Kattni Rembor for Adafruit Industries
# SPDX-License-Identifier: MIT

# 2022 07 16 preparing to refactor

"""
This code runs a NeoTrellis with a Feather M4 processor. Other processors and more boards may come later
This code uses both the adafruit.neopixel library (for on-board single pixel) and the adafruit_seesaw.neopixel.
It will blink all the pixels on startup
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

# setup single pixel strip if board has it, blink it once
onboard_neopixel.setup_onboard_neopixel()

# create the i2c object for the trellis
# note the use of busio.I2C() instead of board.I2C()
# apparently this is an issue for M4 (rPi Pico too?)
i2c_bus = busio.I2C(board.SCL, board.SDA)
trellis = NeoTrellis(i2c_bus)

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
