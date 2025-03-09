"""
OLED Real-Time Clock Display

This program initializes an SSD1306 OLED display connected via SPI interface and continuously displays the current time in real-time.
It uses the `luma.oled` library to communicate with the OLED display and the `datetime` module to fetch and format the current time.

Steps:
1. Initializes the SPI interface and OLED device using the specified GPIO pins for DC (Data/Command) and RST (Reset).
2. Continuously fetches the current time in the format "HH:MM:SS".
3. Displays the current time on the OLED screen at the coordinates (10, 10).
4. Updates the time every second.
5. The program runs indefinitely until the user interrupts it (e.g., by pressing Ctrl+C).

Dependencies:
- luma.core
- luma.oled
- time
- datetime

Hardware Requirements:
- SSD1306 OLED display connected via SPI.
- GPIO pins for DC (24) and RST (25) as specified in the code.

Usage:
Run the script, and the current time will be displayed on the OLED screen in real-time. The program will continue running until manually stopped.
"""


from luma.core.interface.serial import spi
from luma.core.render import canvas
from luma.oled.device import ssd1306
import time
from datetime import datetime

# Initialize SPI and OLED device
serial = spi(device=0, port=0, gpio_DC=24, gpio_RST=25)
device = ssd1306(serial)

try:
    while True:
        # Get the current time
        current_time = datetime.now().strftime("%H:%M:%S")
        
        # Display the current time on the OLED
        with canvas(device) as draw:
            draw.text((10, 10), f"Time: {current_time}", fill="white")
        
        # Wait for 1 second before updating
        time.sleep(1)

except KeyboardInterrupt:
    print("Script stopped by user.")