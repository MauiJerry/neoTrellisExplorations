# SPDX-FileCopyrightText: 2021 Kattni Rembor for Adafruit Industries
# SPDX-License-Identifier: MIT

# 2022 07 16 preparing to refactor

"""
This code runs a NeoTrellis with a Feather M4 processor. Other processors and more boards may come later
This code uses both the adafruit.neopixel library (for on-board single pixel) and the adafruit_seesaw.neopixel.
It will blink all the pixels on startup
Then run a DefaultAnimation
When a key is pressed, any animation stops that key's led lights in keyColor[i]
When a key is released, it voids any existing animation and runs animations[i]
OnBoardNeopixel toggles on each press and each release
"""
# not sure why but mu editor/cp keeps doing a reload/soft reboot unless we do this
# so then we have to use Ctrl-D to reload with Mu editor
import supervisor

supervisor.disable_autoreload()
print("autoreload disabled")


import code_NeotrellisExplorations
