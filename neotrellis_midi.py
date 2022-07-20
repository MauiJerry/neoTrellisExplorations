# neotrellis_midi.py
"""
This module provides some midi functions for the neotrellis.
It is used by the neotrellis_keypad to send NoteOn/NoteOff midi messages
an associated key is pressed.  The array
when the keyNotes[] list
"""

import usb_midi
import adafruit_midi
from adafruit_midi.note_on import NoteOn
from adafruit_midi.note_off import NoteOff

# constants for channel, velocity and notes to associate with keys
# caveat: programmers count channels from 0, normal folks count from 1
# you can see difference viewing midi traffic using
#    https://www.kilpatrickaudio.com/apps/midiview/
# we send zero, it receives 0 but prints out 1
#
__midi_channel = 0

# 16 midi notes to associate with keypad by number
__midiNotes = [
    60, 61, 62, 63,
    64, 65, 66, 67,
    68, 69, 70, 71,
    72, 73, 74, 75,
]

__midi = None

def setup_midi():
    global __midi, __midi_channel
    #  MIDI setup as MIDI out device
    print("setup midi out device")
    __midi = adafruit_midi.MIDI(midi_out=usb_midi.ports[1], out_channel=__midi_channel)

def send_note_on(idx):
    global __midi
    print("YO send_note_on", idx, __midi)
    if __midi is None:
        print("Midi not defined")
    else:
        print("send midi NoteOn ", idx, __midiNotes[idx], __midi)
        __midi.send(NoteOn(__midiNotes[idx], 120))

def send_note_off(idx):
    global __midi
    if __midi is None:
        print("Midi not defined")
    else:
        __midi.send(NoteOff(__midiNotes[idx], 120))
        print("send midi NoteOff ", idx, __midiNotes[idx])

