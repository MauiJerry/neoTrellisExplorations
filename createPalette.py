#
"""
This creates a rainbow palette of colors
"""

from math import sqrt, cos, sin, radians

# Remap the calculated rotation to 0 - 255
def remap(vector):
    return int(((255 * vector + 85) * 0.75) + 0.5)

# Calculate the Hue rotation starting with Red as 0 degrees
def rotate(degrees):
    cosA = cos(radians(degrees))
    sinA = sin(radians(degrees))
    red = cosA + (1.0 - cosA) / 3.0
    green = 1./3. * (1.0 - cosA) + sqrt(1./3.) * sinA
    blue = 1./3. * (1.0 - cosA) - sqrt(1./3.) * sinA
    return (remap(red), remap(green), remap(blue))

palette = []
pixels = []
# onBoardPixel

# Generate a rainbow palette with 16 entries
for degree in range(0, 360, int(360/16)):
    print(degree)
    color = rotate(degree)
    palette.append(color[0] << 16 | color[1] << 8 | color[2])

# Create the Pattern
for y in range(0, 4):
    for x in range(0, 4):
        pixels.append(x * 30 + y * -30)

# Clear the screen
print ("created palette of ", len(palette))
for clr in palette:
    print(hex(clr), end=", ")
print("")
print ("created pixels ", pixels)

# here it ran the Animation
