# Raspberry Pi I2C LCD Wiring and Code Explanation

## Overview
This project demonstrates how to interface a 16x2 I2C LCD with a Raspberry Pi using the `RPLCD` library. The LCD displays messages in a loop, and the backlight can be manually controlled via I2C commands.

## Required Components
- Raspberry Pi (any model with I2C support)
- 16x2 I2C LCD (PCF8574 I2C backpack)
- Jumper wires

## Wiring Diagram
Connect the I2C LCD module to the Raspberry Pi as follows:

| LCD (PCF8574) | Raspberry Pi |
|--------------|--------------|
| VCC         | 5V (Pin 2 or 4) |
| GND         | GND (Pin 6 or 9) |
| SDA         | GPIO2 (Pin 3) |
| SCL         | GPIO3 (Pin 5) |

## Installation
Ensure your Raspberry Pi has I2C enabled. You can enable it using:
```bash
sudo raspi-config
```
Navigate to **Interfacing Options** → **I2C** → **Enable**.

## Troubleshooting
- If the LCD is not displaying text, ensure the I2C address is correct by running:
  ```bash
  sudo i2cdetect -y 1
  ```
  The default address is `0x3F`, but some modules use `0x27`.
- Ensure `smbus` and `RPLCD` libraries are installed properly.
- Check wiring connections and ensure I2C is enabled.

## Conclusion
This project showcases how to interface an I2C LCD with a Raspberry Pi, display messages, and control the backlight manually. Happy coding!

> Author: `Araham Abeddin`
