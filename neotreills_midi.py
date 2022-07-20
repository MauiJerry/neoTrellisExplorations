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

# 16 midi notes to associate with keypad by number
midiNotes = [
    60, 61, 62, 63,
    64, 65, 66, 67,
    68, 69, 70, 71,
    72, 73, 74, 75,
]

__midi = None

def setup_midi():
    #  MIDI setup as MIDI out device
    __midi = adafruit_midi.MIDI(midi_out=usb_midi.ports[1], out_channel=0)

def send_note_on(idx):
    __midi.send(NoteOn(midiNotes[idx], 120))

def send_note_off(idx):
    __midi.send(NoteOff(midiNotes[idx], 120))