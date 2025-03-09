"""
OLED Centered QR Code Display Script

This program generates a QR code from a given text and displays it centered on an SSD1306 OLED screen connected via SPI.
The QR code is resized to fit within a 64x64 pixel area and is displayed in monochrome format. The program ensures the QR code is centered on the OLED display (128x64 pixels).

Steps:
1. Initializes the SPI interface and OLED device using the specified GPIO pins for DC (Data/Command) and RST (Reset).
2. Defines the text to be encoded into a QR code (in this case, a Hindi poetic line).
3. Generates a QR code using the `qrcode` library with low error correction (ERROR_CORRECT_L) and a box size of 10 for clarity.
4. Resizes the QR code image to fit within a 64x64 pixel area.
5. Converts the QR code image to monochrome (1-bit) format for compatibility with the OLED display.
6. Calculates the starting position to center the QR code on the OLED screen (128x64 pixels).
7. Displays the QR code on the OLED screen using the `luma.oled` library.
8. Keeps the program running indefinitely to display the QR code until the user interrupts it (e.g., by pressing Ctrl+C).

Dependencies:
- luma.core
- luma.oled
- PIL (Pillow)
- qrcode
- time

Hardware Requirements:
- SSD1306 OLED display connected via SPI.
- GPIO pins for DC (24) and RST (25) as specified in the code.

Usage:
Run the script, and the QR code will be displayed centered on the OLED screen. The program will continue running until manually stopped.
"""

from luma.core.interface.serial import spi
from luma.core.render import canvas
from luma.oled.device import ssd1306
from PIL import Image
import qrcode
import time

# Initialize SPI and OLED device
serial = spi(device=0, port=0, gpio_DC=24, gpio_RST=25)
device = ssd1306(serial)

# Text to convert into QR code
text = (
#    "Sure! How about naming it \"If you want something more creative. 😊"
    "Hello world!"
)

# Generate QR code
qr = qrcode.QRCode(
    version=1,  # Controls the size of the QR code (1 is the smallest)
    error_correction=qrcode.constants.ERROR_CORRECT_L,  # Error correction level
    box_size=10,  # Size of each "box" in the QR code
    border=1,  # Border size in boxes
)
qr.add_data(text)
qr.make(fit=True)

# Create an image from the QR code
qr_image = qr.make_image(fill_color="black", back_color="white")

# Resize the QR code to fit within a 64x64 area
qr_image = qr_image.resize((64, 64), Image.NEAREST)

# Convert the image to monochrome (1-bit) for the OLED display
qr_image = qr_image.convert("1")

# Display the QR code on the OLED (centered in a 128x64 display)
with canvas(device) as draw:
    # Calculate the starting position to center the QR code
    x = (device.width - 64) // 2  # Center horizontally
    y = (device.height - 64) // 2  # Center vertically
    draw.bitmap((x, y), qr_image, fill="white")

# Keep the script running to display the QR code
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Script stopped by user.")
