"""
OLED Shapes Display Script

This program demonstrates how to draw basic shapes (rectangle, circle, and line) on an SSD1306 OLED display 
connected via SPI interface. It uses the `luma.oled` library to communicate with the OLED display.

Steps:
1. Initializes the SPI interface and OLED device using the specified GPIO pins for DC (Data/Command) and RST (Reset).
2. Continuously draws the following shapes on the OLED display:
   - A rectangle with an outline and filled with black.
   - A circle with an outline and filled with black.
   - A horizontal line.
3. The shapes are redrawn every second.
4. The program runs indefinitely until the user interrupts it (e.g., by pressing Ctrl+C).

Dependencies:
- luma.core
- luma.oled
- time

Hardware Requirements:
- SSD1306 OLED display connected via SPI.
- GPIO pins for DC (24) and RST (25) as specified in the code.

Usage:
Run the script, and the shapes (rectangle, circle, and line) will be displayed on the OLED screen. 
The program will continue running until manually stopped.
"""

from luma.core.interface.serial import spi
from luma.core.render import canvas
from luma.oled.device import ssd1306
import time

# Initialize SPI and OLED device
serial = spi(device=0, port=0, gpio_DC=24, gpio_RST=25)
device = ssd1306(serial)

try:
    while True:
        with canvas(device) as draw:
            # Draw a rectangle
            draw.rectangle((10, 10, 50, 50), outline="white", fill="black")
            
            # Draw a circle
            draw.ellipse((60, 10, 100, 50), outline="white", fill="black")
            
            # Draw a line
            draw.line((10, 60, 100, 60), fill="white")
        
        # Wait for 1 second before redrawing
        time.sleep(1)

except KeyboardInterrupt:
    print("Script stopped by user.")
    