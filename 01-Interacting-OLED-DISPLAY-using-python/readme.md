# 1. Wiring of SPI OLED Display with Raspberry Pi
```wiring
GND  → GND (Pin 6)
VCC  → 3.3V (Pin 1)
D0   → GPIO 11 (Pin 23, SCLK)
D1   → GPIO 10 (Pin 19, MOSI)
RES  → GPIO 25 (Pin 22)
DC   → GPIO 24 (Pin 18)
CS   → GPIO 8 (Pin 24, CE0)
```

# 2. Install Required Packages

```bash
# Update and upgrade the system
sudo apt update
sudo apt upgrade -y

# Install necessary packages
sudo apt install python3-pip python3-pil python3-smbus -y

# Install the Luma OLED library
pip3 install luma.oled --break-system-packages

```

# 3. Python Code to Display Text on the OLED

```py
from luma.core.interface.serial import spi
from luma.core.render import canvas
from luma.oled.device import ssd1306
import time

# Initialize SPI and OLED device
serial = spi(device=0, port=0, gpio_DC=24, gpio_RST=25)
device = ssd1306(serial)

# Display text on the OLED
with canvas(device) as draw:
    draw.text((10, 10), "Hello, OLED!", fill="white")

print("Text displayed on OLED!")

# Keep the script running indefinitely
try:
    while True:
        time.sleep(1)  # Keep the program running
except KeyboardInterrupt:
    print("Script stopped by user.")
```

# 4. How to Run:

- Connect the OLED display to the Raspberry Pi as per the wiring diagram.

- Install the required packages using the provided commands.

- Save the Python script (e.g., `oled_display.py`) and run it:

```python
python3 oled_display.py
```

- The text "Hello, OLED!" will appear on the display, and the program will keep running until you stop it with `Ctrl+C`.