"""
I2C LCD with Backlight Control Script

This program controls a 16x2 LCD display connected via I2C to a Raspberry Pi. It demonstrates how to:
1. Initialize the LCD using the `RPLCD` library.
2. Display alternating messages on the LCD.
3. Manually control the LCD backlight using the `smbus` library.

Steps:
1. Initializes the LCD with the I2C address `0x3F` and sets it up for 16 columns and 2 rows.
2. Uses the `smbus` library to manually control the backlight by sending commands to the I2C address.
3. Displays two sets of messages on the LCD, alternating every 3 seconds.
4. Turns off the backlight after displaying each set of messages (optional).
5. Handles a KeyboardInterrupt (Ctrl+C) to gracefully clear the LCD and turn on the backlight before exiting.

Dependencies:
- RPLCD (for LCD control)
- smbus (for I2C communication)
- time (for delays)

Hardware Requirements:
- 16x2 LCD display with I2C interface.
- Raspberry Pi with I2C enabled.
- Correct I2C address (default is 0x3F, but this may vary depending on the LCD module).

Usage:
1. Connect the I2C LCD to the Raspberry Pi.
2. Ensure the I2C address (`0x3F`) matches the address of your LCD module.
3. Run the script, and the LCD will display alternating messages on both lines.
4. The program will continue running until interrupted (e.g., by pressing Ctrl+C).
"""

from RPLCD.i2c import CharLCD
import smbus
import time

# Initialize the LCD
# Replace `0x3F` with your I2C address if it's different
# Replace `i2c_expander='PCF8574'` if your I2C expander is different (e.g., 'PCF8574A')
lcd = CharLCD(i2c_expander='PCF8574', address=0x3F, port=1, cols=16, rows=2, dotsize=8)

# Initialize I2C bus for manual backlight control
bus = smbus.SMBus(1)  # Use 1 for newer Raspberry Pi models, 0 for older ones

def turn_off_backlight():
    # Send command to turn off the backlight
    bus.write_byte(0x3F, 0x00)  # Replace 0x3F with your I2C address

def turn_on_backlight():
    # Send command to turn on the backlight
    bus.write_byte(0x3F, 0x08)  # Replace 0x3F with your I2C address

try:
    # Keep the program running until manually stopped
    while True:

        # Clear the LCD screen
        lcd.clear()

        # Turn off the backlight after writing the text
        turn_off_backlight()

        # Write a message to the LCD
        lcd.write_string("Hello, World!")
        lcd.crlf()  # Move to the next line
        lcd.write_string("Raspberry Pi")

        # Wait for 3 seconds
        time.sleep(3)

        # Clear the screen again
        lcd.clear()

        # Turn off the backlight after writing the text
        turn_off_backlight()

        # Write another message
        lcd.write_string("I2C LCD Demo")
        lcd.crlf()
        lcd.write_string("By Your Name")

        # Turn off the backlight after writing the text
        # turn_off_backlight()

        # Wait for 3 seconds
        time.sleep(3)

except KeyboardInterrupt:
    # When you press Ctrl+C, clear the screen and turn on the backlight
    lcd.clear()
    turn_on_backlight()  # Turn on the backlight before exiting
    print("Program stopped. LCD cleared and backlight turned on.")
