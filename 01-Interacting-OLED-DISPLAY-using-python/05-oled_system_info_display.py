"""
OLED System Info Display Script

This program displays the current time, date, and IP address on an SSD1306 OLED display connected via SPI.
It uses the `luma.oled` library to communicate with the OLED display and the `Pillow` library for font rendering.

Steps:
1. Initializes the SPI interface and OLED device using the specified GPIO pins for DC (Data/Command) and RST (Reset).
2. Retrieves the current time and date using the `datetime` module.
3. Retrieves the device's IP address using the `socket` module.
4. Displays the time, date, and IP address on the OLED screen using the default font.
5. Updates the display every second and keeps the program running indefinitely until interrupted by the user (e.g., Ctrl+C).

Dependencies:
- luma.core
- luma.oled
- Pillow (for font rendering)
- datetime
- socket
- time

Hardware Requirements:
- SSD1306 OLED display connected via SPI.
- GPIO pins for DC (24) and RST (25) as specified in the code.

Usage:
Run the script, and the OLED display will show the current time, date, and IP address. The program will continue running until manually stopped.
"""

from luma.core.interface.serial import spi
from luma.core.render import canvas
from luma.oled.device import ssd1306
import time
from datetime import datetime
from PIL import ImageFont  # Import ImageFont from Pillow
import socket  # Import socket module to get IP address

# Function to get the IP address
def get_ip_address():
    try:
        # Create a socket to get the IP address
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))  # Connect to a public DNS server
        ip_address = s.getsockname()[0]  # Get the IP address
        s.close()
        return ip_address
    except Exception as e:
        return "No IP"

# Initialize SPI and OLED device
serial = spi(device=0, port=0, gpio_DC=24, gpio_RST=25)
device = ssd1306(serial)

# Use the default font
font = ImageFont.load_default()

try:
    while True:
        # Get the current date and time
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")  # Format time as HH:MM:SS
        current_date = now.strftime("%Y-%m-%d")  # Format date as YYYY-MM-DD
        
        # Get the IP address
        ip_address = get_ip_address()
        
        # Display the current time, date, and IP address on the OLED
        with canvas(device) as draw:
            # Display time (default font)
            draw.text((0, 0), f"Time: {current_time}", fill="white", font=font)
            # Display date (default font)
            draw.text((0, 20), f"Date: {current_date}", fill="white", font=font)
            # Display IP address (default font)
            draw.text((0, 40), f"IP: {ip_address}", fill="white", font=font)
        
        # Wait for 1 second before updating
        time.sleep(1)

except KeyboardInterrupt:
    print("Script stopped by user.")