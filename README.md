# NeoTrellisExplorations
 playing with Adafruit NeoTrellis
 
 more extensive documentation on hackaday.io:
   https://hackaday.io/project/186327-neotrellis-explorations

code_ files are intended to run as code.py on CircuitPython device.

Adafruit NeoTrellis PCB
	(url)
  4x4 array of elastomer buttons plus RGB Led on i2c
  some examples online with adafruit but a bit thin
  kit including Feather M4, Button Pad, acrylic case
	(url)
	
Getting animations to run on the NeoTrellis turned out to be a bit difficult. 

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
	
