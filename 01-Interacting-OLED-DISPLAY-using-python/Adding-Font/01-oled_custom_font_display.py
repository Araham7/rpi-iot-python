"""
OLED Custom Font Display Script

This program displays the text "Hello World!" on an SSD1306 OLED screen connected via SPI, using a custom font loaded from a TTF file.
The program demonstrates how to use custom fonts with the `PIL.ImageFont` library to render text on the OLED display.

Steps:
1. Initializes the SPI interface and OLED device using the specified GPIO pins for DC (Data/Command) and RST (Reset).
2. Loads a custom font (MoonDance-Regular.ttf) from the specified path and sets the font size to 12.
3. Enters a loop to continuously display the text "Hello World!" on the OLED screen using the custom font.
4. Keeps the program running indefinitely to display the text until the user interrupts it (e.g., by pressing Ctrl+C).

Dependencies:
- luma.core
- luma.oled
- PIL (Pillow)
- time

Hardware Requirements:
- SSD1306 OLED display connected via SPI.
- GPIO pins for DC (24) and RST (25) as specified in the code.

Usage:
1. Ensure the custom font file (MoonDance-Regular.ttf) is available at the specified path.
2. Run the script, and the text "Hello World!" will be displayed on the OLED screen using the custom font.
3. The program will continue running until manually stopped.
"""

from luma.core.interface.serial import spi
from luma.core.render import canvas
from luma.oled.device import ssd1306
from PIL import ImageFont
import time

# Initialize SPI and OLED device
serial = spi(device=0, port=0, gpio_DC=24, gpio_RST=25)
device = ssd1306(serial)

# Load a custom font (update the path to your font file)
font = ImageFont.truetype("./Moon_Dance/MoonDance-Regular.ttf", size=12)

try:
    while True:
        with canvas(device) as draw:
            # Display text using the custom font
            draw.text((10, 10), "Hello World!", font=font, fill="white")
        
        time.sleep(1)

except KeyboardInterrupt:
    print("Script stopped by user.")
