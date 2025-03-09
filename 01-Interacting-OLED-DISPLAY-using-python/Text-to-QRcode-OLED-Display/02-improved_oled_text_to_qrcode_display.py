"""
OLED QR Code Display Script

This program generates a QR code from a given text and displays it on an SSD1306 OLED screen connected via SPI.
The QR code is resized to fit the OLED display's resolution (128x64 pixels) and is displayed in monochrome format.

Steps:
1. Initializes the SPI interface and OLED device using the specified GPIO pins for DC (Data/Command) and RST (Reset).
2. Defines the text to be encoded into a QR code.
3. Generates a QR code using the `qrcode` library with high error correction for better reliability.
4. Resizes the QR code image to fit the OLED screen dimensions (128x64 pixels).
5. Converts the QR code image to monochrome (1-bit) format for compatibility with the OLED display.
6. Displays the QR code on the OLED screen using the `luma.oled` library.
7. Keeps the program running indefinitely to display the QR code until the user interrupts it (e.g., by pressing Ctrl+C).

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
Run the script, and the QR code will be displayed on the OLED screen. The program will continue running until manually stopped.
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
text = "Araham: Together in kindness & unity. 🌟"  # Use shorter text for better scannability

# Generate QR code
qr = qrcode.QRCode(
    version=2,  # Increase version for more data capacity
    error_correction=qrcode.constants.ERROR_CORRECT_H,  # High error correction
    box_size=4,  # Adjust box_size for better fit
    border=1,  # Border size in boxes
)
qr.add_data(text)
qr.make(fit=True)

# Create an image from the QR code
qr_image = qr.make_image(fill_color="black", back_color="white")

# Resize the QR code to fit the full screen (128x64 pixels)
qr_image = qr_image.resize((128, 64), Image.NEAREST)

# Convert the image to monochrome (1-bit) for the OLED display
qr_image = qr_image.convert("1")

# Display the QR code on the OLED (full screen)
with canvas(device) as draw:
    draw.bitmap((0, 0), qr_image, fill="white")  # Start at (0, 0) for full screen

# Keep the script running to display the QR code
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Script stopped by user.")
