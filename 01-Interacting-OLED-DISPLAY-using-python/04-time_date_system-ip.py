"""
OLED System Info Display Script

This program displays the current time, date, and IP address on an SSD1306 OLED display connected via SPI.
It uses the `luma.oled` library to communicate with the OLED display and the `socket` module to fetch the IP address.

Steps:
1. Initializes the SPI interface and OLED device using the specified GPIO pins for DC (Data/Command) and RST (Reset).
2. Fetches the current time, date, and IP address.
3. Displays the time, date, and IP address on the OLED screen.
4. Updates the display every second.
5. Runs indefinitely until the user interrupts it (e.g., by pressing Ctrl+C).

Dependencies:
- luma.core
- luma.oled
- time
- datetime
- Pillow (PIL) for font handling (if needed in the future)
- socket for fetching the IP address

Hardware Requirements:
- SSD1306 OLED display connected via SPI.
- GPIO pins for DC (24) and RST (25) as specified in the code.

Usage:
Run the script, and the current time, date, and IP address will be displayed on the OLED screen. The program will continue running until manually stopped.
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
            # Display time (default size)
            draw.text((0, 0), f"Time: {current_time}", fill="white")
            # Display date (default size)
            draw.text((0, 20), f"Date: {current_date}", fill="white")
            # Display IP address (default size)
            draw.text((0, 40), f"IP: {ip_address}", fill="white")
        
        # Wait for 1 second before updating
        time.sleep(1)

except KeyboardInterrupt:
    print("Script stopped by user.")
    