# OLED Custom Font Display Script

## Overview
This project demonstrates how to display text using a custom font on an SSD1306 OLED display connected via SPI to a Raspberry Pi. The script utilizes the `PIL.ImageFont` library to render text on the OLED screen with a TrueType Font (TTF).

## Features
- Displays "Hello World!" using a custom font on the SSD1306 OLED screen.
- Uses SPI communication for efficient data transfer.
- Runs indefinitely until manually stopped by the user.

## Requirements
### Hardware
- Raspberry Pi (any model with SPI support)
- SSD1306 OLED Display (SPI version)
- Jumper wires

### Software Dependencies
Ensure the following Python libraries are installed:
```sh
pip3 install luma.core luma.oled pillow
```

## Wiring Connections
Connect the OLED display to the Raspberry Pi GPIO as follows:

| OLED Pin | Raspberry Pi GPIO Pin |
|----------|----------------------|
| VCC      | 3.3V (Pin 1)         |
| GND      | GND (Pin 6)          |
| DIN (MOSI) | GPIO 10 (Pin 19)   |
| CLK (SCK) | GPIO 11 (Pin 23)    |
| DC       | GPIO 24 (Pin 18)     |
| RST      | GPIO 25 (Pin 22)     |
| CS       | GPIO 8 (Pin 24)      |

## Installation & Usage
1. Clone or download the script.
2. Ensure the custom font file `MoonDance-Regular.ttf` is available at the specified path(i.e, `./Moon_Dance/MoonDance-Regular.ttf`).
3. Run the script using:
```sh
python oled_display.py
```
4. The OLED screen will display "Hello World!" using the custom font.
5. Press `Ctrl+C` to stop the script.

## Code Explanation
### Initialization
- The script initializes the SPI interface and OLED device using `luma.oled`.
- A custom font (`MoonDance-Regular.ttf`) is loaded using `PIL.ImageFont.truetype`.

### Display Loop
- The script enters an infinite loop where it continuously displays "Hello World!" on the OLED screen using the custom font.
- It refreshes every second.
- The program exits safely when `Ctrl+C` is pressed.

## Troubleshooting
- **No display output?** Check the wiring connections and ensure SPI is enabled in Raspberry Pi settings (`sudo raspi-config`).
- **Font not found error?** Ensure the `MoonDance-Regular.ttf` file exists at the specified path.
- **Permission issues?** Try running the script with `sudo`.

## License
This project is open-source. Feel free to modify and distribute it.

## Author
`Araham Abeddin`

