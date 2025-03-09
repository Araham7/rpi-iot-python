"""
I2C LCD Scrolling Text Script

This program controls a 16x2 LCD display connected via I2C to a Raspberry Pi. It demonstrates how to:
1. Initialize the LCD using the `RPLCD` library.
2. Scroll long text messages on both lines of the LCD.
3. Handle a KeyboardInterrupt (Ctrl+C) to gracefully clear the LCD and exit the program.

Key Features:
- The text on the first line (line 0) scrolls completely before the text on the second line (line 1) starts scrolling.
- The scrolling effect is achieved by adding padding (spaces) to the text and displaying a 16-character substring at a time.
- The scrolling speed can be adjusted using the `delay` parameter in the `scroll_text` function.

Steps:
1. Initializes the LCD with the I2C address `0x3F` and sets it up for 16 columns and 2 rows.
2. Defines a `scroll_text` function to scroll text on a specific line of the LCD.
3. Uses an infinite loop to continuously scroll two messages on the LCD, alternating between the first and second lines.
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
3. Run the script, and the LCD will scroll the messages on both lines.
4. The program will continue running until interrupted (e.g., by pressing Ctrl+C).
"""


# Important NOTE:---
#. (1). With the help of the below code when the text of the 1st-line(i.e, 0th-row) gets completely scrolled then the 2nd-line(i.e, 1st-row) text will be scroll.
#. (2). Then the 1st and then 2nd line text scroll and so on it will gets repeated.

from RPLCD.i2c import CharLCD  # Import the CharLCD class from the RPLCD library
import time  # Import the time library for delays

# Initialize the LCD
lcd = CharLCD(i2c_expander='PCF8574', address=0x3F, port=1, cols=16, rows=2, dotsize=8)  # Set up the LCD with I2C address 0x3F

def scroll_text(text, line=0, delay=0.3):  # Function to scroll text on a specific line
    padding = " " * 16  # Add 16 spaces to the text to create a scrolling effect
    text_with_padding = padding + text + padding  # Combine the text with padding
    for i in range(len(text_with_padding) - 15):  # Loop through the text
        lcd.cursor_pos = (line, 0)  # Move cursor to the specified line
        lcd.write_string(text_with_padding[i:i+16])  # Display a 16-character substring
        time.sleep(delay)  # Add a delay to control the scrolling speed

try:  # Start a try block to handle exceptions
    while True:  # Run an infinite loop
        # Scroll a long message on the first line
        scroll_text("This is line 1 scrolling!", line=0, delay=0.3)  # Scroll on line 1
        # Scroll a long message on the second line
        scroll_text("This is line 2 scrolling!", line=1, delay=0.3)  # Scroll on line 2

except KeyboardInterrupt:  # Handle a KeyboardInterrupt (Ctrl+C) to gracefully exit the program
    lcd.clear()  # Clear the LCD screen before exiting
    print("Program stopped. LCD cleared.")  # Print a message to the console
