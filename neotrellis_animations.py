# neotrellis_animations.py
"""
this module encapsulates some example code to drive adafruit_led_animations on a NeoTrellis
most of it was ripped off from adafruit_led_animations.examples.led_animation_all_animations
Note pixels will be seesaw.neopixel, not regular neopixel
A 'fixed' version of seesaw.neopixel is requried from a branch
that derives seesaw.neopixel from PixelBuf (neopixel strip)
see https://github.com/adafruit/Adafruit_CircuitPython_seesaw/pull/106

"""
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

from onboard_neopixel import blinkOnBoardPixel

# a local reference to the neotrellis.pixels PixelBuf derived NeoPixel
__trellis_pixels = None
__allBlack = None
__trellis_pixel_columns = None
__trellis_pixel_rows = None

# we have Color.BLACK as well as the other color names (and colorwheel() ) from led_animations
# we need a 16 color palette that does NOT contain black - one for each button in keypad
rainbowPalette = [
    0xa0002, 0x80004, 0x50007, 0x30009,
    0xb, 0x10b, 0x308, 0x606,
    0x804, 0xb01, 0xb00, 0x30900,
    0x50700, 0x70400, 0xa0200, 0xc0000
]

def print_rainbowPalette():
    print("Rainbow Palette:", rainbowPalette)
    print("Rainbow Palette: ", end=" ")
    for clr in rainbowPalette:
        print(hex(clr), end=", ")
    print()

def show_rainbowPalette():
    global __trellis_pixels
    print_rainbowPalette()
    print("RainbowPalete blinking on board pixel")
    for clr in rainbowPalette:
        print("clr ", hex(clr))
        BLINK_COLOR = clr
        __trellis_pixels.fill(clr)
        blinkOnBoardPixel()

# define some module variables
current_animation = None
trellisAnimations = []

# this init function creates a bunch of animations in the trellisAnimations[]
def setup_animations(neotrellis):
    global __allBlack
    global __trellis_pixels
    global __trellis_pixel_columns
    global __trellis_pixel_rows

    __trellis_pixels = neotrellis.pixels
    __trellis_pixels.fill(Color.WHITE)
    #trellis.pixels.fill(Color.BLACK)
    blink = Blink(__trellis_pixels, speed=0.5, color=Color.JADE)
    color_cycle = ColorCycle(__trellis_pixels, speed=0.4, colors=[Color.MAGENTA, Color.ORANGE])
    comet = Comet(__trellis_pixels, speed=0.1, color=Color.PURPLE, tail_length=4, bounce=True)
    chase = Chase(__trellis_pixels, speed=0.1, size=3, spacing=6, color=Color.WHITE)
    pulse = Pulse(__trellis_pixels, speed=0.1, period=3, color=Color.AMBER)
    sparkle = Sparkle(__trellis_pixels, speed=0.1, color=Color.PURPLE, num_sparkles=6)
    solid = Solid(__trellis_pixels, color=Color.JADE)
    rainbow = Rainbow(__trellis_pixels, speed=0.1, period=2)
    sparkle_pulse = SparklePulse(__trellis_pixels, speed=0.1, period=3, color=Color.JADE)
    rainbow_comet = RainbowComet(__trellis_pixels, speed=0.1, tail_length=16, bounce=True)
    rainbow_chase = RainbowChase(__trellis_pixels, speed=0.1, size=3, spacing=2, step=8)
    rainbow_sparkle = RainbowSparkle(__trellis_pixels, speed=0.1, num_sparkles=4)
    custom_color_chase = CustomColorChase(
        __trellis_pixels, speed=0.1, size=2, spacing=3,
        colors=[Color.ORANGE, Color.WHITE, Color.JADE]
    )

    # thats only 13 built in!  need 16 to have one each key
    allWhite = Solid(__trellis_pixels, color=Color.WHITE)
    allBlack = Solid(__trellis_pixels, color=Color.BLACK)
    __allBlack = allBlack
    allGray = Solid(__trellis_pixels, color=(8,8,2))
    allOrange = Solid(__trellis_pixels, color=Color.ORANGE)
    allRed= Solid(__trellis_pixels, color=Color.RED)
    allBlue = Solid(__trellis_pixels, color=Color.BLUE)
    allGold = Solid(__trellis_pixels, color=Color.GOLD)

    # create some pixelMaps for rows and columns
    __trellis_pixel_columns = helper.PixelMap.vertical_lines(
        __trellis_pixels, 4, 4, helper.horizontal_strip_gridmap(4, alternating=False)
    )
    __trellis_pixel_rows = helper.PixelMap.horizontal_lines(
        __trellis_pixels, 4, 4, helper.horizontal_strip_gridmap(4, alternating=False)
    )

    # and build some animations using PixelMaps (from example, mod for size)
    comet_h = Comet(__trellis_pixel_rows, speed=0.1, color=Color.PURPLE, tail_length=3, bounce=True)
    comet_v = Comet(__trellis_pixel_columns, speed=0.1, color=Color.AMBER, tail_length=6, bounce=True)
    chase_h = Chase(__trellis_pixel_rows, speed=0.1, size=3, spacing=6, color=Color.JADE)
    rainbow_v = Rainbow(__trellis_pixel_columns, speed=0.1, period=2)
    rainbow_chase_v = RainbowChase(__trellis_pixel_columns, speed=0.1, size=3, spacing=2, step=8)
    rainbow_chase_h = RainbowChase(__trellis_pixel_rows, speed=0.1, size=3, spacing=3)
    rainbow_comet_v = RainbowComet(__trellis_pixel_columns, speed=0.1, tail_length=7, bounce=True)

    # build an array of all those animation, first 16 will be tied to keypad actions later
    global trellisAnimations
    trellisAnimations = [
        # first 16 will match to key pad index 0-15
        blink, color_cycle, comet, chase,
        pulse, sparkle, comet_h, rainbow,
        sparkle_pulse, rainbow_comet, rainbow_chase, rainbow_sparkle,
        custom_color_chase, rainbow_chase_v, rainbow_chase_h, rainbow_comet_v,
        # any more are just filler here
        allWhite, allBlack, allRed, allBlue, allGold, allOrange, allGray,
        chase_h, comet_v, rainbow_v,
    ]

    # start with simple solid Gray animation
    global current_animation
    current_animation = allGray

    print ("animations setup current_animation: ", current_animation)

def set_all_black_animation():
    global current_animation
    global __allBlack
    current_animation = __allBlack
    current_animation = __allBlack

def set_animation_byIndex(idx):
    global current_animation
    if idx in range(len(trellisAnimations)):
        current_animation = trellisAnimations[idx]

def freeze():
    global current_animation
    current_animation.freeze()

def resume():
    global current_animation
    print ("resume current_animation: ", current_animation)
    current_animation.resume()

