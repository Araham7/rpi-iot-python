# OLED Centered QR Code Display

## Description
This script generates a QR code from a given text and displays it centered on an SSD1306 OLED screen connected via SPI. The QR code is resized to fit within a 64x64 pixel area and is displayed in monochrome format. The program ensures the QR code is centered on the OLED display (128x64 pixels).

## Features
- Initializes the SPI interface and OLED device using specified GPIO pins.
- Generates a QR code from a user-defined text.
- Uses a QR code with low error correction for optimal clarity.
- Resizes and converts the QR code for compatibility with the OLED display.
- Centers the QR code on the 128x64 OLED screen.
- Runs indefinitely until interrupted by the user.

## Dependencies
Ensure you have the following Python libraries installed:
- `luma.core`
- `luma.oled`
- `Pillow` (PIL)
- `qrcode`
- `time`

Install dependencies using pip:
```bash
pip install luma.core luma.oled pillow qrcode[pil]
```

## Hardware Requirements
- SSD1306 OLED display connected via SPI.
- GPIO pins for SPI communication:
  - **DC (Data/Command):** GPIO 24
  - **RST (Reset):** GPIO 25

## Setup & Wiring
Connect the SSD1306 OLED display to the Raspberry Pi:
- **VCC** → 3.3V
- **GND** → GND
- **DIN (MOSI)** → GPIO 10
- **CLK (SCK)** → GPIO 11
- **CS** → GPIO 8
- **DC** → GPIO 24
- **RST** → GPIO 25

## Usage
1. Clone this repository or copy the script.
2. Run the script using Python:
```bash
python oled_qr_display.py
```
3. The QR code will be displayed centered on the OLED screen.
4. To stop the script, press **Ctrl + C**.

## Code Overview
### 1. Initialize SPI and OLED Device
```python
serial = spi(device=0, port=0, gpio_DC=24, gpio_RST=25)
device = ssd1306(serial)
```
### 2. Generate QR Code
```python
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=1,
)
qr.add_data("Hello world!")
qr.make(fit=True)
```
### 3. Resize and Convert to Monochrome
```python
qr_image = qr.make_image(fill_color="black", back_color="white")
qr_image = qr_image.resize((64, 64), Image.NEAREST)
qr_image = qr_image.convert("1")
```
### 4. Center and Display on OLED
```python
with canvas(device) as draw:
    x = (device.width - 64) // 2
    y = (device.height - 64) // 2
    draw.bitmap((x, y), qr_image, fill="white")
```
### 5. Keep the Script Running
```python
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Script stopped by user.")
```

## Notes
- The text for the QR code can be modified in the script.
- Make sure your SPI interface is enabled on the Raspberry Pi (`raspi-config`).

## License
This project is open-source and licensed under the MIT License.

