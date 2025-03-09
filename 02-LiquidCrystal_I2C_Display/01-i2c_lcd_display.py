"""
I2C LCD Display Script

This program controls a 16x2 LCD display connected via I2C to a Raspberry Pi. It demonstrates how to initialize the LCD, send commands, and display text on both lines of the LCD.

Steps:
1. Initializes the I2C connection to the LCD using the specified I2C address and bus.
2. Defines constants for LCD commands, line addresses, and timing.
3. Provides functions to:
   - Initialize the LCD (`lcd_init`).
   - Send data or commands to the LCD (`lcd_byte`).
   - Toggle the enable pin for communication (`lcd_toggle_enable`).
   - Display a string on a specific line of the LCD (`lcd_string`).
4. In the main loop, displays two sets of messages on the LCD, alternating every 3 seconds.
5. Clears the LCD display when the program is interrupted or exits.

Dependencies:
- smbus (for I2C communication)
- time (for delays)

Hardware Requirements:
- 16x2 LCD display with I2C interface.
- Raspberry Pi with I2C enabled.
- Correct I2C address (default is 0x3F, but this may vary depending on the LCD module).

Usage:
1. Connect the I2C LCD to the Raspberry Pi.
2. Ensure the I2C address (`I2C_ADDR`) matches the address of your LCD module.
3. Run the script, and the LCD will display alternating messages on both lines.
4. The program will continue running until interrupted (e.g., by pressing Ctrl+C).
"""

import smbus
import time

# Define I2C address and bus
I2C_ADDR = 0x3F  # Replace with your I2C address
I2C_BUS = 1

# LCD constants
LCD_WIDTH = 16  # Characters per line
LCD_CHR = 1  # Mode - Sending data
LCD_CMD = 0  # Mode - Sending command

LCD_LINE_1 = 0x80  # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0  # LCD RAM address for the 2nd line

LCD_BACKLIGHT = 0x08  # On
# LCD_BACKLIGHT = 0x00  # Off

ENABLE = 0b00000100  # Enable bit

# Timing constants
E_PULSE = 0.0005
E_DELAY = 0.0005

# Open I2C interface
bus = smbus.SMBus(I2C_BUS)

def lcd_init():
    # Initialise display
    lcd_byte(0x33, LCD_CMD)  # 110011 Initialise
    lcd_byte(0x32, LCD_CMD)  # 110010 Initialise
    lcd_byte(0x06, LCD_CMD)  # 000110 Cursor move direction
    lcd_byte(0x0C, LCD_CMD)  # 001100 Display On,Cursor Off, Blink Off
    lcd_byte(0x28, LCD_CMD)  # 101000 Data length, number of lines, font size
    lcd_byte(0x01, LCD_CMD)  # 000001 Clear display
    time.sleep(E_DELAY)

def lcd_byte(bits, mode):
    # Send byte to data pins
    # bits = the data
    # mode = 1 for data, 0 for command

    bits_high = mode | (bits & 0xF0) | LCD_BACKLIGHT
    bits_low = mode | ((bits << 4) & 0xF0) | LCD_BACKLIGHT

    # High bits
    bus.write_byte(I2C_ADDR, bits_high)
    lcd_toggle_enable(bits_high)

    # Low bits
    bus.write_byte(I2C_ADDR, bits_low)
    lcd_toggle_enable(bits_low)

def lcd_toggle_enable(bits):
    # Toggle enable
    time.sleep(E_DELAY)
    bus.write_byte(I2C_ADDR, (bits | ENABLE))
    time.sleep(E_PULSE)
    bus.write_byte(I2C_ADDR, (bits & ~ENABLE))
    time.sleep(E_DELAY)

def lcd_string(message, line):
    # Send string to display
    message = message.ljust(LCD_WIDTH, " ")

    lcd_byte(line, LCD_CMD)

    for i in range(LCD_WIDTH):
        lcd_byte(ord(message[i]), LCD_CHR)

def main():
    # Main program block
    lcd_init()

    while True:
        # Send some test
        lcd_string("Araham Aeddin!", LCD_LINE_1)
        lcd_string("Raspberry Pi", LCD_LINE_2)

        time.sleep(3)  # 3 second delay

        # Send some more text
        lcd_string("I2C LCD Tutorial", LCD_LINE_1)
        lcd_string("Araham Aeddin", LCD_LINE_2)

        time.sleep(3)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
    finally:
        lcd_byte(0x01, LCD_CMD)
