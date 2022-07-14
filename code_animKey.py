# SPDX-FileCopyrightText: 2021 Kattni Rembor for Adafruit Industries
# SPDX-License-Identifier: MIT

"""
This code runs a NeoTrellis with a Feather M4 processor. Other processors and more boards may come later
This code uses both the adafruit.neopixel library (for on-board single pixel) and the adafruit_seesaw.neopixel.
It will blink all the pixels on startup
Then run a DefaultAnimation
When a key is pressed, any animation stops that key's led lights in keyColor[i]
When a key is released, it voids any existing animation and runs animations[i]
OnBoardNeopixel toggles on each press and each release


"""
import board
from board import SCL, SDA
import busio
from adafruit_neotrellis.neotrellis import NeoTrellis

import neopixel
import time

from adafruit_led_animation.animation.blink import Blink
from adafruit_led_animation.animation.sparklepulse import SparklePulse
from adafruit_led_animation.animation.comet import Comet
from adafruit_led_animation.animation.chase import Chase
from adafruit_led_animation.animation.pulse import Pulse
from adafruit_led_animation.animation.sparkle import Sparkle
from adafruit_led_animation.animation.rainbowchase import RainbowChase
from adafruit_led_animation.animation.rainbowsparkle import RainbowSparkle
from adafruit_led_animation.animation.rainbowcomet import RainbowComet
from adafruit_led_animation.animation.solid import Solid
from adafruit_led_animation.animation.colorcycle import ColorCycle
from adafruit_led_animation.animation.rainbow import Rainbow
from adafruit_led_animation.animation.customcolorchase import CustomColorChase
from adafruit_led_animation.sequence import AnimationSequence
#from adafruit_led_animation.color import PURPLE, WHITE, AMBER, JADE, MAGENTA, ORANGE, BLACK
import adafruit_led_animation.color as Color
from adafruit_led_animation import helper

# not sure why but mu editor/cp keeps doing a reload/soft reboot unless we do this
# so then we have to use Ctrl-D to reload with Mu editor
import supervisor
supervisor.disable_autoreload()
print("autoreload disabled")

## begin onboard pixel -----------------------------------------------
# setup the onboard neopixel
# #### from neoPixel - bottom of M4  pixel
PIXEL_PIN = board.D1  # pin that the NeoPixel is connected to
ORDER = neopixel.RGB  # pixel color channel order
BLINK_COLOR = (100, 50, 150)  # color to blink
DELAY = 0.25  # blink rate in seconds

# Create the NeoPixel object
onBoardPixel = None
if 'NEOPIXEL' in board.dir():
    global onBoardPixel
    onBoardPixel = neopixel.NeoPixel(PIXEL_PIN, 1, pixel_order=ORDER)
    print("Board have onboard NEOPIXEL")
else:
    print("Board does NOT have onboard NEOPIXEL")

def blinkOnBoardPixel():
    global onBoardPixel
    if onBoardPixel:
        onBoardPixel[0] = BLINK_COLOR
        time.sleep(DELAY)
        onBoardPixel[0] = Color.BLACK
        time.sleep(DELAY)

blinkOnBoardPixel()

onboardStatus = False
def toggleOnBoardPixel():
    global onboardStatus
    if onBoardPixel:
        if onboardStatus:
            onBoardPixel[0] = CLEAR
            onBoardStatus = False
        else:
            onBoardPixel[0] = BLINK_COLOR
            onboardStatus = True

## end onboard pixel ----------------------------------------------

## begin neoTrellis -----------------------------------------------
# create the i2c object for the trellis
# note the use of busio.I2C() instead of board.I2C()
# apparently this is an issue for M4 (rPi Pico too?)
i2c_bus = busio.I2C(SCL, SDA)

trellis = NeoTrellis(i2c_bus)
# trellis.pixels will be a PixelBuf (neopixel strip)
# with 'fixed' branch of seesaw.neopixel, this will work
# see https://github.com/adafruit/Adafruit_CircuitPython_seesaw/pull/106
# Note these will be seesaw.neopixel, not regular neopixel

# create some pixelMaps
trellis_pixel_columns = helper.PixelMap.vertical_lines(
    pixels, 4, 1, helper.horizontal_strip_gridmap(8, alternating=False)
)
trellis_pixel_rows = helper.PixelMap.horizontal_lines(
    pixels, 4, 1, helper.horizontal_strip_gridmap(8, alternating=False)
)

# need a 16 color palette that does NOT contain black - one each button
rainbowPalette = [
    '#D0021B', '#FF001B', '#FD7281', '#F5A623', '#D38C16', '#F2CD91', '#918612', '#FFE800', '#FDF5A7',
    '#417505', '# 7ED321', '#D5FFA8', '#053874', '#4A90E2', '#96C6FD', '#400C6C', '#8B03FF', '#D1ABF2'
]
# we have Color.BLACK as well as the other color names (and colorwheel)

# create semi unique animation for each key
blink = Blink(trellis.pixels, speed=0.9, color=Color.JADE)
color_cycle = ColorCycle(trellis.pixels, speed=0.4, colors=[Color.MAGENTA, Color.ORANGE])
comet = Comet(trellis.pixels, speed=0.1, color=Color.PURPLE, tail_length=4, bounce=True)
chase = Chase(trellis.pixels, speed=0.1, size=3, spacing=6, color=Color.WHITE)
pulse = Pulse(trellis.pixels, speed=0.1, period=3, color=Color.AMBER)
sparkle = Sparkle(trellis.pixels, speed=0.1, color=Color.PURPLE, num_sparkles=10)
solid = Solid(trellis.pixels, color=Color.JADE)
rainbow = Rainbow(trellis.pixels, speed=0.1, period=2)
sparkle_pulse = SparklePulse(trellis.pixels, speed=0.1, period=3, color=Color.JADE)
rainbow_comet = RainbowComet(trellis.pixels, speed=0.1, tail_length=4, bounce=True)
rainbow_chase = RainbowChase(trellis.pixels, speed=0.1, size=3, spacing=2, step=8)
rainbow_sparkle = RainbowSparkle(trellis.pixels, speed=0.1, num_sparkles=10)
custom_color_chase = CustomColorChase(
    trellis.pixels, speed=0.1, size=2, spacing=3, colors=[Color.ORANGE, Color.WHITE, Color.JADE]
)

# thats only 13 built in!  need 16 to have one each key
allWhite = Solid(trellis.pixels, color=Color.WHITE)
allOrange = Solid(trellis.pixels, color=Color.ORANGE)
allRed= Solid(trellis.pixels, color=Color.RED)
allBlue = Solid(trellis.pixels, color=Color.BLUE)
allGold = Solid(trellis.pixels, color=Color.GOLD)

current_animation = allWhite
#ToDO: create some row/colunm animationss

# arrays to map key index to animation and colors
keyColors = rainbowPalette
keyAnimations = [
    blink, color_cycle, comet, chase,
    pulse, sparkle, solid, rainbow,
    sparkle_pulse, rainbow_comet, rainbow_chase, rainbow_sparkle,
    custom_color_chase, allRed, allBlue, allGold
]

# -------- Key Handling ---------

# this will be called when button events are received
def doKey(event):
    if event.edge == NeoTrellis.EDGE_RISING:
        # pressed: toggle, stop, color my pixel, set current animation
        toggleOnBoardPixel()
        # stop current animation
        current_animation.freeze()
        #trellis.pixels.fill(Color.BLACK)
        trellis.pixels[event.number] = keyColors[event.number]
        #current_animation = keyAnimations[event.number]
    # turn the LED off when a falling edge is detected
    elif event.edge == NeoTrellis.EDGE_FALLING:
        toggleOnBoardPixel()
        #trellis.pixels[event.number] = Color.BLACK
        current_animation = keyAnimations[event.number]

for i in range(16):
    # activate rising edge events on all keys
    trellis.activate_key(i, NeoTrellis.EDGE_RISING)
    # activate falling edge events on all keys
    trellis.activate_key(i, NeoTrellis.EDGE_FALLING)
    # set all keys to trigger the doKey() callback
    trellis.callbacks[i] = doKey

# --------------- Main Loop ------------

i = 0
while True:
    current_animation.animate()
    # call the sync function call any triggered callbacks
    trellis.sync()
    # the trellis can only be read every 17 millisecons or so
    time.sleep(0.02)
    i +=1
    if i%100 == 0:
        print(i, end='.')
    if i%10000 == 0:
        print(i, "reset")
        i=0
