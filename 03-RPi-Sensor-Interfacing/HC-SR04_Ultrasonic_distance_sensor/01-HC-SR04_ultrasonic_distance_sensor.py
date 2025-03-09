
Copy
"""
HC-SR04 Ultrasonic Distance Sensor Script

This program measures distance using an HC-SR04 ultrasonic sensor connected to a Raspberry Pi. It demonstrates how to:
1. Initialize the GPIO pins for the HC-SR04 sensor.
2. Send a trigger pulse to the sensor and measure the echo pulse duration.
3. Calculate the distance based on the echo pulse duration.
4. Continuously measure and display the distance in centimeters.

Steps:
1. Sets up the GPIO pins for the HC-SR04 sensor (Trig and Echo).
2. Defines a `get_distance` function to:
   - Send a 10-microsecond trigger pulse to the sensor.
   - Measure the duration of the echo pulse.
   - Calculate the distance using the speed of sound (343 m/s or 17150 cm/s).
3. Continuously measures and prints the distance every second.
4. Handles a KeyboardInterrupt (Ctrl+C) to gracefully clean up the GPIO pins and exit the program.

Dependencies:
- RPi.GPIO (for GPIO control)
- time (for delays and timing)

Hardware Requirements:
- HC-SR04 Ultrasonic Sensor.
- Raspberry Pi with GPIO pins.
- Voltage divider circuit (if Echo pin voltage exceeds 3.3V).

Wiring:
- VCC  → 5V (Pin 2 or 4)
- GND  → GND (Pin 6 or 9)
- Trig → GPIO23 (Pin 16)
- Echo → Voltage Divider → GPIO12 (Pin 32)

Usage:
1. Connect the HC-SR04 sensor to the Raspberry Pi as per the wiring instructions.
2. Run the script, and the program will continuously measure and display the distance in centimeters.
3. The program will continue running until interrupted (e.g., by pressing Ctrl+C).
"""

import RPi.GPIO as GPIO
import time

# GPIO Pin Setup
TRIG = 23
ECHO = 12

# Initialize GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

def get_distance():
    # Send a short pulse to trigger the sensor
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    # Wait for the echo pulse to start
    while GPIO.input(ECHO) == 0:
        pulse_start = time.time()

    # Wait for the echo pulse to end
    while GPIO.input(ECHO) == 1:
        pulse_end = time.time()

    # Calculate distance (in cm)
    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150  # Speed of sound in cm/s
    distance = round(distance, 2)

    return distance

try:
    while True:
        dist = get_distance()
        print(f"Distance: {dist} cm")
        time.sleep(1)  # Wait 1 second before next reading

except KeyboardInterrupt:
    print("Measurement stopped by user")
    GPIO.cleanup()
