"""
I2C LCD Simultaneous Scrolling Text Script

This program controls a 16x2 LCD display connected via I2C to a Raspberry Pi. It demonstrates how to:
1. Initialize the LCD using the `RPLCD` library.
2. Scroll two different text messages simultaneously on both lines of the LCD.
3. Repeat the scrolling effect indefinitely until the program is interrupted.

Key Features:
- The text on both lines scrolls simultaneously, creating a dynamic display effect.
- The scrolling effect is achieved by adding padding (spaces) to the text and displaying a 16-character substring at a time.
- The scrolling speed can be adjusted using the `delay` parameter in the `scroll_text` function.
- The program repeats the scrolling effect continuously until interrupted.

Steps:
1. Initializes the LCD with the I2C address `0x3F` and sets it up for 16 columns and 2 rows.
2. Defines a `scroll_text` function to scroll text on a specific line of the LCD using a generator.
3. Defines a `scroll_both_lines` function to scroll two lines simultaneously using generators.
4. Uses an infinite loop to continuously scroll two messages on the LCD.
5. Handles a KeyboardInterrupt (Ctrl+C) to gracefully clear the LCD and exit the program.

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
3. Run the script, and the LCD will scroll two messages simultaneously on both lines.
4. The program will continue running until interrupted (e.g., by pressing Ctrl+C).
"""


#. Imprtant NOTE :---
#. (1). Through this code text will be scrolling on the both line at the same time .
#. (2). Same text will be reapeting after cmpletely scrolling the text.

from RPLCD.i2c import CharLCD  # Import the CharLCD class from the RPLCD library
import time  # Import the time library for delays

# Initialize the LCD
lcd = CharLCD(i2c_expander='PCF8574', address=0x3F, port=1, cols=16, rows=2, dotsize=8)  # Set up the LCD with I2C address 0x3F

def scroll_text(text, line, delay=0.3):  # Function to scroll text on a specific line
    padding = " " * 16  # Add 16 spaces to the text to create a scrolling effect
    text_with_padding = padding + text + padding  # Combine the text with padding
    for i in range(len(text_with_padding) - 15):  # Loop through the text
        lcd.cursor_pos = (line, 0)  # Move cursor to the specified line
        lcd.write_string(text_with_padding[i:i+16])  # Display a 16-character substring
        yield  # Pause execution and return control to the caller

def scroll_both_lines(text1, text2, delay=0.3):  # Function to scroll two lines simultaneously
    # Create generators for scrolling each line
    scroll_line1 = scroll_text(text1, line=0, delay=delay)
    scroll_line2 = scroll_text(text2, line=1, delay=delay)

    # Loop until both lines finish scrolling
    while True:
        try:
            next(scroll_line1)  # Scroll the first line
            next(scroll_line2)  # Scroll the second line
            time.sleep(delay)  # Add a delay to control the scrolling speed
        except StopIteration:  # Exit when both lines finish scrolling
            break

try:  # Start a try block to handle exceptions
    while True:  # Run an infinite loop
        # Scroll two lines simultaneously
        scroll_both_lines("<1>Stay curious, learn more!", "<2>Innovate, create, inspire!", delay=0.3)

except KeyboardInterrupt:  # Handle a KeyboardInterrupt (Ctrl+C) to gracefully exit the program
    lcd.clear()  # Clear the LCD screen before exiting
    print("Program stopped. LCD cleared.")  # Print a message to the console
