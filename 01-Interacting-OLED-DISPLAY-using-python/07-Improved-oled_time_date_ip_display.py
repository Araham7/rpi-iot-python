"""
OLED Time, Date, and IP Display Script

This program displays the current time, date, and IP address on an SSD1306 OLED display connected via SPI.
It uses the `luma.oled` library to communicate with the OLED display and the `PIL` library for custom font rendering.

Key Features:
1. Displays the current time in HH:MM:SS format.
2. Displays the current date in DD-MM-YYYY format.
3. Fetches and displays the device's IP address.
4. Uses custom fonts for better readability (DejaVuSans.ttf is preferred).
5. Dynamically calculates text positions to ensure proper alignment and spacing.

Dependencies:
- luma.core
- luma.oled
- PIL (Pillow)
- datetime
- socket
- time

Hardware Requirements:
- SSD1306 OLED display connected via SPI.
- GPIO pins for DC (24) and RST (25) as specified in the code.

Usage:
1. Run the script.
2. The OLED display will show the current time, date, and IP address.
3. The program updates every second and runs indefinitely until stopped by the user (e.g., by pressing Ctrl+C).

Custom Fonts:
- The program attempts to load the "DejaVuSans.ttf" font for better display quality.
- If the font is not found, it falls back to the default font.

IP Address:
- The program fetches the device's IP address using a socket connection.
- If the IP address cannot be retrieved, it displays "No IP".

Exit:
- The program can be stopped by pressing Ctrl+C, and it cleans up the OLED display before exiting.
"""

from luma.core.interface.serial import spi
from luma.core.render import canvas
from luma.oled.device import ssd1306
import time
from datetime import datetime
from PIL import ImageFont
import socket

def get_ip_address():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip_address = s.getsockname()[0]
        s.close()
        return ip_address
    except Exception as e:
        return "No IP"

# Initialize SPI and OLED
serial = spi(device=0, port=0, gpio_DC=24, gpio_RST=25)
device = ssd1306(serial)

# Custom font settings
try:
    font_main = ImageFont.truetype("DejaVuSans.ttf", 14)  # Main font (Time and Date)
    font_ip = ImageFont.truetype("DejaVuSans.ttf", 13)     # IP font (1px smaller)
except IOError:
    print("Custom font not found, using default")
    font_main = ImageFont.load_default()
    font_ip = ImageFont.load_default()

def calculate_y_positions():
    # Use getbbox to calculate positions
    bbox_main = font_main.getbbox("Test")  # For main font
    bbox_ip = font_ip.getbbox("Test")      # For IP font
    
    height_main = bbox_main[3] - bbox_main[1]  # Height of main font
    height_ip = bbox_ip[3] - bbox_ip[1]        # Height of IP font
    
    line_spacing = 6  # Increase gap between lines (पहले 2 था, अब 6 कर दिया)
    
    return [
        (0, 0),  # Time position
        (0, height_main + line_spacing),  # Date position
        (0, height_main + line_spacing + height_ip + line_spacing)  # IP position
    ]

try:
    y_positions = calculate_y_positions()
    
    while True:
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        current_date = now.strftime("%d-%m-%Y")  # DD-MM-YYYY format
        ip_address = get_ip_address()

        with canvas(device) as draw:
            # Render text with updated positions and fonts
            draw.text(y_positions[0], f"Time: {current_time}", fill="white", font=font_main)
            draw.text(y_positions[1], f"Date: {current_date}", fill="white", font=font_main)
            draw.text(y_positions[2], f"IP: {ip_address[:15]}", fill="white", font=font_ip)  # Use smaller font for IP

        time.sleep(1)

except KeyboardInterrupt:
    print("Script stopped by user.")
    device.cleanup()