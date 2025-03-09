"""
OLED Display Text Script

This program initializes an SSD1306 OLED display connected via SPI interface and displays the text "Hello, OLED!" on the screen. 
It uses the `luma.oled` library to communicate with the OLED display.

Steps:
1. Initializes the SPI interface and OLED device using the specified GPIO pins for DC (Data/Command) and RST (Reset).
2. Uses the `canvas` context to draw the text "Hello, OLED!" at the coordinates (10, 10) on the OLED display.
3. Prints a confirmation message in the console once the text is displayed.
4. Keeps the program running indefinitely until the user interrupts it (e.g., by pressing Ctrl+C).

Dependencies:
- luma.core
- luma.oled
- time

Hardware Requirements:
- SSD1306 OLED display connected via SPI.
- GPIO pins for DC (24) and RST (25) as specified in the code.

Usage:
Run the script, and the text "Hello, OLED!" will be displayed on the OLED screen. The program will continue running until manually stopped.
"""

from luma.core.interface.serial import spi
from luma.core.render import canvas
from luma.oled.device import ssd1306
import time

# Initialize SPI and OLED device
serial = spi(device=0, port=0, gpio_DC=24, gpio_RST=25)
device = ssd1306(serial)

# Display text on the OLED
with canvas(device) as draw:
    draw.text((10, 10), "Hello, OLED!", fill="white")

print("Text displayed on OLED!")

# Keep the script running indefinitely
try:
    while True:
        time.sleep(1)  # Keep the program running
except KeyboardInterrupt:
    print("Script stopped by user.")
