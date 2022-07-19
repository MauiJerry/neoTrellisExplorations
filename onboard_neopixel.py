# onboard_neopixel.py :
"""
This code module (onBoard_Neopixel) provides access to the onboard single neopixel
available on certain CircuitPython boards. onBoardPixel (reference), blink(), toggle()
The Adafruit Feather M4 Express, Adafruit QT Py RP2040 are examples of such boards.
The Raspberry Pi Pico does not have an onboard neopixels
"""

import board
import neopixel
import time
import adafruit_led_animation.color as Color

BLINK_COLOR = (100, 50, 150)  # color to blink, allow change
DELAY = 0.25  # blink rate in seconds

# Create the NeoPixel object for the onBoard pixel,
# check if processor board supports it
# note this will be regular NeoPixel strip of length 1, not a seesaw.NeoPixel
onBoardPixel = None
if 'NEOPIXEL' in dir(board):
    onBoardPixel = neopixel.NeoPixel( board.NEOPIXEL, 1, pixel_order=neopixel.GRB)
    print("Board have onboard NEOPIXEL", onBoardPixel)
else:
    print("Board does NOT have onboard NEOPIXEL")

def blinkOnBoardPixel(color=BLINK_COLOR):
    global onBoardPixel
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
def toggleOnBoardPixel(color=BLINK_COLOR):
    global __onboardStatus
    global onBoardPixel
    if onBoardPixel:
        if __onboardStatus:
            onBoardPixel.fill((0,0,0))
            __onboardStatus = False
        else:
            onBoardPixel.fill(color)
            __onboardStatus = True

# end onboard pixel ----------------------------------------------
