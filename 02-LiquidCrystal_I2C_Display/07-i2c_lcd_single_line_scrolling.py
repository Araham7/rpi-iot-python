"""
I2C LCD Single Line Scrolling Script

This program controls a 16x2 LCD display connected via I2C to a Raspberry Pi. It demonstrates how to:
1. Initialize the LCD using the `RPLCD` library.
2. Scroll a long text message on the first line of the LCD.
3. Handle a KeyboardInterrupt (Ctrl+C) to gracefully clear the LCD and exit the program.

Key Features:
- The text scrolls horizontally on the first line of the LCD.
- The scrolling effect is achieved by adding padding (spaces) to the text and displaying a 16-character substring at a time.
- The scrolling speed can be adjusted using the `delay` parameter in the `scroll_text` function.

Steps:
1. Initializes the LCD with the I2C address `0x3F` and sets it up for 16 columns and 2 rows.
2. Defines a `scroll_text` function to scroll text on the first line of the LCD.
3. Uses an infinite loop to continuously scroll a long message on the LCD.
4. Handles a KeyboardInterrupt (Ctrl+C) to gracefully clear the LCD and exit the program.

Dependencies:
- RPLCD (for LCD control)
- time (for delays)

Hardware Requirements:
- 16x2 LCD display with I2C interface.
- Raspberry Pi with I2C enabled.
- Correct I2C address (default is 0x3F, but this may vary depending on the LCD module).

Usage:
1. Connect the I2C LCD to the Raspberry Pi.
2. Ensure the I2C address (`0x3F`) matches the address of your LCD module.
3. Run the script, and the LCD will scroll the message on the first line.
4. The program will continue running until interrupted (e.g., by pressing Ctrl+C).
"""


from RPLCD.i2c import CharLCD  # Import the CharLCD class from the RPLCD library
import time  # Import the time library for delays

# Initialize the LCD
lcd = CharLCD(i2c_expander='PCF8574', address=0x3F, port=1, cols=16, rows=2, dotsize=8)  # Set up the LCD with I2C address 0x3F

# note :---
# (1). set > ```delay=0.2``` for ``Faster scrolling``.
# (2. set > ````delay=0.5``` for ``Slower scrolling``.
def scroll_text(text, delay=0.2):  # Function to scroll text on the LCD
    padding = " " * 16  # Add 16 spaces to the text to create a scrolling effect
    text_with_padding = padding + text + padding  # Combine the text with padding
    for i in range(len(text_with_padding) - 15):  # Loop through the text
        lcd.clear()  # Clear the LCD screen
        lcd.write_string(text_with_padding[i:i+16])  # Display a 16-character substring
        time.sleep(delay)  # Add a delay to control the scrolling speed

try:  # Start a try block to handle exceptions
    while True:  # Run an infinite loop
        # Scroll a long message on the LCD
        scroll_text("Error 404: Sleep Not Found! 😴")  # Call the scroll_text function

except KeyboardInterrupt:  # Handle a KeyboardInterrupt (Ctrl+C) to gracefully exit the program
    lcd.clear()  # Clear the LCD screen before exiting
    print("Program stopped. LCD cleared.")  # Print a message to the console
