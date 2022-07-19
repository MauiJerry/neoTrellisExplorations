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
import adafruit_led_animation.color as Color

# local modules
import neotrellis_animations
from onboard_neopixel import onBoardPixel, blinkOnBoardPixel, toggleOnBoardPixel

# begin neoTrellis -----------------------------------------------
# create the i2c object for the trellis
# note the use of busio.I2C() instead of board.I2C()
# apparently this is an issue for M4 (rPi Pico too?)
i2c_bus = busio.I2C(board.SCL, board.SDA)

trellis = NeoTrellis(i2c_bus)

# setup neopixel stuff first
neotrellis_animations.setup_animations(trellis)

# -------- Key Pad Handling ---------
# could be module but short enough for inline
# arrays to map key index to animation and colors
keyColors = neotrellis_animations.rainbowPalette
keyAnimations = neotrellis_animations.trellisAnimations

# doKey() will be called when button events are received
def doKey(event):
    print("\nKeyEvent: ", str(event), " event number",event.number, " edge:",event.edge)
    if event.edge == NeoTrellis.EDGE_RISING:
        # pressed: toggle, stop/freeze current animation, color my pixel
        onBoardPixel[0] = keyColors[event.number]
        #toggleOnBoardPixel()
        # stop current animation, set all to black
        trellis.pixels.fill(Color.BLACK)
        neotrellis_animations.freeze()
        neotrellis_animations.set_all_black_animation()
        neotrellis_animations.resume()
        trellis.pixels[event.number] = keyColors[event.number]
        print("pixel color", hex(keyColors[event.number]))
        trellis.pixels.show()
        blinkOnBoardPixel(keyColors[event.number])

    # start animationwhen a falling edge is detected
    elif event.edge == NeoTrellis.EDGE_FALLING:
        #toggleOnBoardPixel()
        onBoardPixel[0] = Color.BLACK
        trellis.pixels.fill(Color.BLACK)
        #trellis.pixels[event.number] = Color.BLACK
        neotrellis_animations.set_animation_byIndex(event.number)
        neotrellis_animations.current_animation.resume()
        print("new animation", neotrellis_animations.current_animation)

# associate 16 trellis keys with doKey() for both press and release
for i in range(16):
    # activate rising edge events on all keys; key pressed
    trellis.activate_key(i, NeoTrellis.EDGE_RISING)
    # activate falling edge events on all keys; key released
    trellis.activate_key(i, NeoTrellis.EDGE_FALLING)
    # set all keys to trigger the doKey() callback
    trellis.callbacks[i] = doKey

# --------------- Ready for Main Loop ------------
# but first lets print out the key colors
print("key colors", keyColors)
for clr in keyColors:
    print(hex(clr),end=", ")
print("")
print("Setup Complete enter loop ", neotrellis_animations.current_animation)

i = 0
while True:
    neotrellis_animations.current_animation.animate()
    # call the sync function call any triggered callbacks, after the animate()
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
