# neotrellis_keypad.py
"""
Modularized example to setup and handle keypad actions on an adafruit_neotrellis
each key of 4x4 neotrellis has a keyColor that is displayed when it is pressed
each key has an animation (of all 16 neopixels on neotrellis) that plays when releaseds
"""
from adafruit_neotrellis.neotrellis import NeoTrellis
import adafruit_led_animation.color as Color

# local modules
import onboard_neopixel
import neotrellis_animations

keyColors = None
keyAnimations = None

__trellis = None

# could be module but short enough for inline
# arrays to map key index to animation and colors
def setup_keypad(trellis):
    global keyColors
    global keyAnimations
    global __trellis
    __trellis = trellis
    keyColors = neotrellis_animations.rainbowPalette
    keyAnimations = neotrellis_animations.trellisAnimations
    # associate 16 trellis keys with doKey() for both press and release
    for i in range(16):
        # activate rising edge events on all keys; key pressed
        __trellis.activate_key(i, NeoTrellis.EDGE_RISING)
        # activate falling edge events on all keys; key released
        __trellis.activate_key(i, NeoTrellis.EDGE_FALLING)
        # set all keys to trigger the doKey() callback
        __trellis.callbacks[i] = doKey

    # --------------- Ready for Main Loop ------------
    # but first lets print out the key colors
    print("key colors", keyColors)
    for clr in keyColors:
        print(hex(clr), end=", ")
    print("")


# doKey() will be called when button events are received
def doKey(event):
    print("\nKeyEvent: ", str(event), " event number",event.number, " edge:",event.edge)
    if event.edge == NeoTrellis.EDGE_RISING:
        # pressed: toggle, stop/freeze current animation, color my pixel
        onboard_neopixel.on_board_neopixel[0] = keyColors[event.number]
        #toggleOnBoardPixel()
        # freeze current animation, set all to black, just the one to its keyColor
        neotrellis_animations.freeze()
        __trellis.pixels.fill(Color.BLACK)
        __trellis.pixels[event.number] = keyColors[event.number]
        print("pixel color", hex(keyColors[event.number]))
        __trellis.pixels.show()
        # blink onboard with same color
        onboard_neopixel.blinkOnBoardPixel(keyColors[event.number])

    # start animationwhen a falling edge is detected
    elif event.edge == NeoTrellis.EDGE_FALLING:
        #toggleOnBoardPixel()
        onboard_neopixel.on_board_neopixel[0] = Color.BLACK
        __trellis.pixels.fill(Color.BLACK)
        #trellis.pixels[event.number] = Color.BLACK
        neotrellis_animations.set_animation_byIndex(event.number)
        neotrellis_animations.current_animation.resume()
        print("new animation", neotrellis_animations.current_animation)

