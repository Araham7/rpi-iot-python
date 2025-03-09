"""
OLED Date and Time Display Script

This program initializes an SSD1306 OLED display connected via SPI interface and continuously displays the current date and time on the screen.
It uses the `luma.oled` library to communicate with the OLED display and the `datetime` module to fetch the current date and time.

Steps:
1. Initializes the SPI interface and OLED device using the specified GPIO pins for DC (Data/Command) and RST (Reset).
2. Continuously fetches the current date and time using the `datetime` module.
3. Formats the time as "HH:MM:SS" and the date as "YYYY-MM-DD".
4. Displays the formatted time and date on the OLED screen using the `canvas` context.
5. Updates the display every second.
6. The program runs indefinitely until the user interrupts it (e.g., by pressing Ctrl+C).

Dependencies:
- luma.core
- luma.oled
- datetime
- time

Hardware Requirements:
- SSD1306 OLED display connected via SPI.
- GPIO pins for DC (24) and RST (25) as specified in the code.

Usage:
Run the script, and the current date and time will be displayed on the OLED screen. The program will continue running until manually stopped.
"""

from luma.core.interface.serial import spi
from luma.core.render import canvas
from luma.oled.device import ssd1306
import time
from datetime import datetime
from PIL import ImageFont  # Import ImageFont from Pillow

# Initialize SPI and OLED device
serial = spi(device=0, port=0, gpio_DC=24, gpio_RST=25)
device = ssd1306(serial)

try:
    while True:
        # Get the current date and time
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")  # Format time as HH:MM:SS
        current_date = now.strftime("%Y-%m-%d")  # Format date as YYYY-MM-DD
        
        # Display the current time and date on the OLED
        with canvas(device) as draw:
            # Display time (default size)
            draw.text((0, 0), f"Time: {current_time}", fill="white")
            # Display date (default size)
            draw.text((0, 20), f"Date: {current_date}", fill="white")
        
        # Wait for 1 second before updating
        time.sleep(1)

except KeyboardInterrupt:
    print("Script stopped by user.")
