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
5. Handles a KeyboardInterrupt (Ctrl+C) to gracefully clear the LCD and turn off the backlight before exiting.

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


from RPLCD.i2c import CharLCD  # Import the CharLCD class from the RPLCD library
import smbus  # Import the smbus library for I2C communication
import time  # Import the time library for delays

# Initialize the LCD
lcd = CharLCD(i2c_expander='PCF8574', address=0x3F, port=1, cols=16, rows=2, dotsize=8)  # Set up the LCD with I2C address 0x3F

# Initialize I2C bus for manual backlight control
bus = smbus.SMBus(1)  # Use I2C bus 1 (for newer Raspberry Pi models)

def turn_off_backlight():
    bus.write_byte(0x3F, 0x00)  # Send command to turn off the backlight (I2C address 0x3F)

def turn_on_backlight():
    bus.write_byte(0x3F, 0x08)  # Send command to turn on the backlight (I2C address 0x3F)

try:  # Start a try block to handle exceptions
    while True:  # Run an infinite loop
        lcd.clear()  # Clear the LCD screen to remove any previous content
        turn_off_backlight()  # Turn off the backlight after writing the text (optional)

        message1 = "Hello, World!"  # Define the first message to display on the LCD
        message2 = "Raspberry Pi"  # Define the second message to display on the LCD (next line)

        print(f"Sending message: {message1}")  # Print the first message to the console for debugging
        lcd.write_string(message1)  # Write the first message to the LCD screen
        lcd.crlf()  # Move the cursor to the next line (carriage return + line feed)
        print(f"Sending message: {message2}")  # Print the second message to the console for debugging
        lcd.write_string(message2)  # Write the second message to the LCD screen

        time.sleep(3)  # Wait for 3 seconds before proceeding to the next step

        lcd.clear()  # Clear the LCD screen again to prepare for the next set of messages
        turn_off_backlight()  # Turn off the backlight after writing the text (optional)

        message3 = "I2C LCD Demo"  # Define the third message to display on the LCD
        message4 = "By Araham!"  # Define the fourth message to display on the LCD (next line)

        print(f"Sending message: {message3}")  # Print the third message to the console for debugging
        lcd.write_string(message3)  # Write the third message to the LCD screen
        lcd.crlf()  # Move the cursor to the next line (carriage return + line feed)
        print(f"Sending message: {message4}")  # Print the fourth message to the console for debugging
        lcd.write_string(message4)  # Write the fourth message to the LCD screen

        time.sleep(3)  # Wait for 3 seconds before repeating the loop

except KeyboardInterrupt:  # Handle a KeyboardInterrupt (Ctrl+C) to gracefully exit the program
    lcd.clear()  # Clear the LCD screen before exiting
    turn_off_backlight()  # Turn off the backlight before exiting (optional)
    print("Program stopped. LCD cleared and backlight turned on.")  # Print a message to the console
