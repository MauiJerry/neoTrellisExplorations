# NeoTrellisExplorations
 playing with Adafruit NeoTrellis
 
 more extensive documentation on hackaday.io:
   https://hackaday.io/project/186327-neotrellis-explorations

Adafruit NeoTrellis PCB
	Adafruit NeoTrellis RGB Driver PCB for 4x4 Keypad
	https://www.adafruit.com/product/3954
  4x4 array of elastomer buttons plus RGB Led on i2c
  some examples online with adafruit but a bit thin
  kit including Feather M4, Button Pad, acrylic case
	Adafruit 4x4 NeoTrellis Feather M4 Kit Pack
	https://www.adafruit.com/product/4352
	
Getting animations to run on the NeoTrellis turned out to be a bit difficult. The current release of adafruit_seesaw libary has its own version of NeoPixel class that does Not derive from PixelBuf, as do other versions. This precludes use of the rather nice adafruit_led_animations library.
Neradoc on Adafruit's Discord quickly built a branch of seesaw that does derive from PixelBuf.  There isnt much testing yet but its a great advancement.

TODO: refactoring code to module files



examples/code_ files are intended to run as code.py on CircuitPython device.

code_neotrellis_example_m4.py: 
	basic adafruit.neotrellis.example with mods to run a Feather M4. 
	
code_m4_onBoardNeoPixel.py:
	example code to blink colors onboard the CircuitPython device (if available)
	
code_myAllAnimations.py:
	adafruit_led_animations.examples modified for NeoTrellis and Feather M4
	NOTE: requires branch version of adafruit_seesaw library to make seesaw.Neopixel work like adafruit_neopixel (derive from PixelBuf)

code_animKey.py
	animations tied to keypad press
	
code_animKey_PixelMaps.py:
	animations tied to keypad, 
	adds row/column PixelMap animations
	
