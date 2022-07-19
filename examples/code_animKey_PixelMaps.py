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
from adafruit_led_animation import helper
import adafruit_led_animation.color as Color

# not sure why but mu editor/cp keeps doing a reload/soft reboot unless we do this
# so then we have to use Ctrl-D to reload with Mu editor
import supervisor
supervisor.disable_autoreload()
print("autoreload disabled")

## begin with onboard neoPixel if supported
# setup the onboard neopixel
# #### from neoPixel - bottom of M4  pixel
BLINK_COLOR = (100, 50, 150)  # color to blink
DELAY = 0.25  # blink rate in seconds

# Create the NeoPixel object, check if processor board supports it
# note this will be real, regular NeoPixel strip of length 1
on_board_neopixel = None
if 'NEOPIXEL' in dir(board):
    on_board_neopixel = neopixel.NeoPixel(board.NEOPIXEL, 1, pixel_order=neopixel.GRB)
    print("Board have onboard NEOPIXEL", on_board_neopixel)
else:
    print("Board does NOT have onboard NEOPIXEL")

def blinkOnBoardPixel(color=BLINK_COLOR):
    global on_board_neopixel
    if onBoardPixel:
        onBoardPixel.fill(color)
        onBoardPixel.show()
        time.sleep(DELAY)
        onBoardPixel[0] = Color.BLACK
        time.sleep(DELAY)
        onBoardPixel.show()
    else:
        print("No onBoardPixel to blink")

# blink it once to show we here
blinkOnBoardPixel()

__onboardStatus = False
def toggleOnBoardPixel():
    global __onboardStatus
    if on_board_neopixel:
        if onboardStatus:
            on_board_neopixel.fill(Color.BLACK)
            onboardStatus = False
        else:
            on_board_neopixel.fill(BLINK_COLOR)
            onboardStatus = True

# end onboard pixel ----------------------------------------------

# begin neoTrellis -----------------------------------------------
# create the i2c object for the trellis
# note the use of busio.I2C() instead of board.I2C()
# apparently this is an issue for M4 (rPi Pico too?)
i2c_bus = busio.I2C(SCL, SDA)

trellis = NeoTrellis(i2c_bus)
# trellis.pixels will be a PixelBuf (neopixel strip)
# with 'fixed' branch of seesaw.neopixel, this will work
# see https://github.com/adafruit/Adafruit_CircuitPython_seesaw/pull/106
# Note these will be seesaw.neopixel, not regular neopixel
# we have Color.BLACK as well as the other color names (and colorwheel() )

trellis.pixels.fill(Color.WHITE)
#trellis.pixels.fill(Color.BLACK)

# want a 16 color palette that does NOT contain black - one each button
rainbowPalette = [
    0xa0002, 0x80004, 0x50007, 0x30009,
    0xb, 0x10b, 0x308, 0x606,
    0x804, 0xb01, 0xb00, 0x30900,
    0x50700, 0x70400, 0xa0200, 0xc0000
]

print("Rainbow Palette:", rainbowPalette)
print("Rainbow Palette: ", end=" ")
for clr in rainbowPalette:
    print(hex(clr), end=", ")
print()

#=====================================================================================
print("RainbowPalete blinking on board pixel")
for clr in rainbowPalette:
    print("clr ", hex(clr))
    BLINK_COLOR = clr
    trellis.pixels.fill(clr)
    blinkOnBoardPixel()

# create semi unique animation for each key
blink = Blink(trellis.pixels, speed=0.5, color=Color.JADE)
color_cycle = ColorCycle(trellis.pixels, speed=0.4, colors=[Color.MAGENTA, Color.ORANGE])
comet = Comet(trellis.pixels, speed=0.1, color=Color.PURPLE, tail_length=4, bounce=True)
chase = Chase(trellis.pixels, speed=0.1, size=3, spacing=6, color=Color.WHITE)
pulse = Pulse(trellis.pixels, speed=0.1, period=3, color=Color.AMBER)
sparkle = Sparkle(trellis.pixels, speed=0.1, color=Color.PURPLE, num_sparkles=6)
solid = Solid(trellis.pixels, color=Color.JADE)
rainbow = Rainbow(trellis.pixels, speed=0.1, period=2)
sparkle_pulse = SparklePulse(trellis.pixels, speed=0.1, period=3, color=Color.JADE)
rainbow_comet = RainbowComet(trellis.pixels, speed=0.1, tail_length=16, bounce=True)
rainbow_chase = RainbowChase(trellis.pixels, speed=0.1, size=3, spacing=2, step=8)
rainbow_sparkle = RainbowSparkle(trellis.pixels, speed=0.1, num_sparkles=4)
custom_color_chase = CustomColorChase(
    trellis.pixels, speed=0.1, size=2, spacing=3,
    colors=[Color.ORANGE, Color.WHITE, Color.JADE]
)

# thats only 13 built in!  need 16 to have one each key
allWhite = Solid(trellis.pixels, color=Color.WHITE)
allBlack = Solid(trellis.pixels, color=Color.BLACK)
allGray = Solid(trellis.pixels, color=(8,8,2))
allOrange = Solid(trellis.pixels, color=Color.ORANGE)
allRed= Solid(trellis.pixels, color=Color.RED)
allBlue = Solid(trellis.pixels, color=Color.BLUE)
allGold = Solid(trellis.pixels, color=Color.GOLD)

# create some pixelMaps for rows and columns
trellis_pixel_columns = helper.PixelMap.vertical_lines(
    trellis.pixels, 4, 4, helper.horizontal_strip_gridmap(4, alternating=False)
)
trellis_pixel_rows = helper.PixelMap.horizontal_lines(
    trellis.pixels, 4, 4, helper.horizontal_strip_gridmap(4, alternating=False)
)

# and build some animations using PixelMaps (from example, mod for size)
comet_h = Comet(trellis_pixel_rows, speed=0.1, color=Color.PURPLE, tail_length=3, bounce=True)
comet_v = Comet(trellis_pixel_columns, speed=0.1, color=Color.AMBER, tail_length=6, bounce=True)
chase_h = Chase(trellis_pixel_rows, speed=0.1, size=3, spacing=6, color=Color.JADE)
rainbow_chase_v = RainbowChase(trellis_pixel_columns, speed=0.1, size=3, spacing=2, step=8)
rainbow_comet_v = RainbowComet(trellis_pixel_columns, speed=0.1, tail_length=7, bounce=True)
rainbow_v = Rainbow(trellis_pixel_columns, speed=0.1, period=2)
rainbow_chase_h = RainbowChase(trellis_pixel_rows, speed=0.1, size=3, spacing=3)

current_animation = allGray

# -------- Key Pad Handling ---------
# arrays to map key index to animation and colors
keyColors = rainbowPalette
keyAnimations = [
    blink, color_cycle, comet, chase,
    pulse, sparkle, solid, rainbow,
    sparkle_pulse, rainbow_comet, rainbow_chase, rainbow_sparkle,
    custom_color_chase, rainbow_chase_v, rainbow_chase_h, rainbow_comet_v
]

# doKey() will be called when button events are received
def doKey(event):
    global current_animation
    print("\nKeyEvent: ", str(event), " event number",event.number, " edge:",event.edge)
    if event.edge == NeoTrellis.EDGE_RISING:
        # pressed: toggle, stop/freeze current animation, color my pixel
        on_board_neopixel[0] = keyColors[event.number]
        #toggleOnBoardPixel()
        # stop current animation
        current_animation.freeze()
        trellis.pixels.fill(Color.BLACK)
        trellis.pixels[event.number] = keyColors[event.number]
        print("pixel color", hex(keyColors[event.number]))
        trellis.pixels.show()
        blinkOnBoardPixel(keyColors[event.number])
        #current_animation = keyAnimations[event.number]

    # start animationwhen a falling edge is detected
    elif event.edge == NeoTrellis.EDGE_FALLING:
        #toggleOnBoardPixel()
        on_board_neopixel[0] = Color.BLACK
        trellis.pixels.fill(Color.BLACK)
        #trellis.pixels[event.number] = Color.BLACK
        current_animation = keyAnimations[event.number]
        current_animation.resume()
        print("new animation", current_animation)

for i in range(16):
    # activate rising edge events on all keys
    trellis.activate_key(i, NeoTrellis.EDGE_RISING)
    # activate falling edge events on all keys
    trellis.activate_key(i, NeoTrellis.EDGE_FALLING)
    # set all keys to trigger the doKey() callback
    trellis.callbacks[i] = doKey

# --------------- Main Loop ------------
print("key colors", keyColors)
for clr in keyColors:
    print(hex(clr),end=", ")
print("")
print("Setup Complete enter loop ", current_animation)

i = 0
while True:
    current_animation.animate()
    # call the sync function call any triggered callbacks
    trellis.sync()
    # the trellis can only be read every 17 millisecons or so
    #time.sleep(0.02)
    i +=1
    if i%50 == 0:
        print(i, end='.')
    if i%10000 == 0:
        print(i, "reset")
        i=0
