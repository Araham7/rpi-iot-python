"""
OLED Text Scroller Script

This program displays a scrolling text message on an SSD1306 OLED display connected via SPI interface.
The text moves from right to left, creating a scrolling effect. When the text completely scrolls off the screen,
it resets to the right side and continues scrolling indefinitely.

Steps:
1. Initializes the SPI interface and OLED device using the specified GPIO pins for DC (Data/Command) and RST (Reset).
2. Defines the text message to be displayed.
3. Uses a loop to continuously update the position of the text, creating a scrolling effect.
4. Resets the text position to the right side of the screen once it fully scrolls off the left side.
5. Adjusts the scrolling speed using a delay (0.05 seconds in this case).
6. Stops the program when the user interrupts it (e.g., by pressing Ctrl+C).

Dependencies:
- luma.core
- luma.oled
- time

Hardware Requirements:
- SSD1306 OLED display connected via SPI.
- GPIO pins for DC (24) and RST (25) as specified in the code.

Usage:
Run the script, and the text "This is a scrolling text message!" will scroll across the OLED screen.
The program will continue running until manually stopped.
"""

from luma.core.interface.serial import spi
from luma.core.render import canvas
from luma.oled.device import ssd1306
import time

# Initialize SPI and OLED device
serial = spi(device=0, port=0, gpio_DC=24, gpio_RST=25)
device = ssd1306(serial)

# Text to display
text = "This is a scrolling text message!"

try:
    position = 0  # Starting position of the text
    while True:
        with canvas(device) as draw:
            # Draw the text at the current position
            draw.text((position, 10), text, fill="white")
        
        # Update the position for scrolling
        position -= 1  # Move text to the left
        if position < -len(text) * 8:  # Reset position when text scrolls off the screen
            position = device.width  # Reset to the right side of the screen
        
        time.sleep(0.05)  # Adjust the speed of scrolling

except KeyboardInterrupt:
    print("Script stopped by user.")