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


examples/code_XX files are intended to run as code.py on CircuitPython device. they were tests leading to this

code.py:
	entry opened by CircuitPython, invokes other modules

code_NeotrellisExplorations.py:
	what code.py imports to run everything

onboard_neopixel.py:
	set up on main board neopixel, if cpy board has it
	blinks in colors on demand

neotrellis_animations.py:
	sets up animations from adafruit_led_animations
	in an array to be invoked by keypad etc

neotrellis_midi.py:
	sets up midi with 16 note values to sendOn/Off

neotrellis_keypad.py:
	handles neotrellis keypad actions
	starts animations, sends midi keyOn/Off
