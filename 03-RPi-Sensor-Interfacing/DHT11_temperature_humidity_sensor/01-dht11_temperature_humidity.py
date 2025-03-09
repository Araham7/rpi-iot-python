"""
DHT11 Temperature and Humidity Sensor Script

This program reads temperature and humidity data from a DHT11 sensor connected to a Raspberry Pi. It demonstrates how to:
1. Initialize the DHT11 sensor using the Adafruit_DHT library.
2. Continuously read and display temperature and humidity data.
3. Handle a KeyboardInterrupt (Ctrl+C) to gracefully exit the program.

Steps:
1. Sets up the DHT11 sensor on the specified GPIO pin (GPIO4, Pin 7 on the Raspberry Pi).
2. Uses the `Adafruit_DHT.read_retry` function to read temperature and humidity data from the sensor.
3. Prints the temperature and humidity values to the console.
4. Waits for 2 seconds before taking the next reading.
5. Handles a KeyboardInterrupt (Ctrl+C) to gracefully exit the program.

Dependencies:
- Adafruit_DHT (for DHT11 sensor communication)
- time (for delays)

Hardware Requirements:
- DHT11 Temperature and Humidity Sensor.
- Raspberry Pi with GPIO pins.

Wiring:
- VCC  → 3.3V (Pin 1 on the Raspberry Pi)
- GND  → GND (Pin 6 on the Raspberry Pi)
- Data → GPIO4 (Pin 7 on the Raspberry Pi)

Usage:
1. Connect the DHT11 sensor to the Raspberry Pi as per the wiring instructions.
2. Run the script, and the program will continuously read and display temperature and humidity data.
3. The program will continue running until interrupted (e.g., by pressing Ctrl+C).
"""

import Adafruit_DHT
import time

# Set the sensor type and GPIO pin
sensor = Adafruit_DHT.DHT11
pin = 4  # GPIO4 (Pin 7 on the Raspberry Pi)

try:
    while True:
        # Try to read the sensor data
        humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

        if humidity is not None and temperature is not None:
            print(f"Temperature: {temperature:.1f}°C, Humidity: {humidity:.1f}%")
        else:
            print("Failed to retrieve data from the sensor.")

        # Wait for 2 seconds before the next reading
        time.sleep(2)

except KeyboardInterrupt:
    print("Program stopped by user.")
