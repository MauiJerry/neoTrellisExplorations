# onboard_neopixel.py :
"""
This code module (onBoard_Neopixel) provides access to the onboard single neopixel
available on certain CircuitPython boards. onBoardPixel (reference), blink(), toggle()
The Adafruit Feather M4 Express, Adafruit QT Py RP2040 are examples of such boards.
The Raspberry Pi Pico does not have an onboard neopixel
"""

import board
import neopixel
import time
import adafruit_led_animation.color as Color

BLINK_COLOR = (100, 50, 150)  # color to blink, allow change
DELAY = 0.25  # blink rate in seconds

on_board_neopixel = None
def setup_onboard_neopixel():
    global on_board_neopixel
    # Create the NeoPixel object for the onBoard pixel,
    # check if processor board supports it
    # note this will be regular NeoPixel strip of length 1, not a seesaw.NeoPixel like on neotrellis
    if 'NEOPIXEL' in dir(board):
        on_board_neopixel = neopixel.NeoPixel(board.NEOPIXEL, 1, pixel_order=neopixel.GRB)
        print("Board have onboard NEOPIXEL", on_board_neopixel)
    else:
        print("Board does NOT have onboard NEOPIXEL")
    # blink it once to show we here
    blinkOnBoardPixel()

def blinkOnBoardPixel(color=BLINK_COLOR):
    global on_board_neopixel
    if on_board_neopixel:
        on_board_neopixel.fill(color)
        on_board_neopixel.show()
        time.sleep(DELAY)
        on_board_neopixel[0] = (0,0,0)
        time.sleep(DELAY)
        on_board_neopixel.show()
    else:
        print("No onBoardPixel to blink")

__onboardStatus = False
def toggleOnBoardPixel(color=BLINK_COLOR):
    global __onboardStatus
    global on_board_neopixel
    if on_board_neopixel:
        if __onboardStatus:
            on_board_neopixel.fill((0, 0, 0))
            __onboardStatus = False
        else:
            on_board_neopixel.fill(color)
            __onboardStatus = True

# end onboard pixel ----------------------------------------------
