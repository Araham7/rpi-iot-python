# DHT11 Temperature and Humidity Sensor Script

## Overview
This script reads temperature and humidity data from a DHT11 sensor connected to a Raspberry Pi. It continuously retrieves and displays sensor readings while handling potential errors and allowing a graceful exit.

## Features
- Initializes and reads data from the DHT11 sensor using the `Adafruit_DHT` library.
- Continuously fetches and prints temperature and humidity data.
- Waits 2 seconds between readings.
- Handles `KeyboardInterrupt` (Ctrl+C) to exit the program cleanly.

## Prerequisites
### Hardware Requirements
- Raspberry Pi with GPIO pins
- DHT11 Temperature and Humidity Sensor
- Jumper wires

### Software Requirements
- Raspberry Pi OS (or any Linux-based OS for Raspberry Pi)
- Python 3 installed
- `Adafruit_DHT` library (for DHT sensor communication)

## Wiring Instructions
| DHT11 Pin | Raspberry Pi Pin |
|-----------|----------------|
| VCC       | 3.3V (Pin 1)   |
| GND       | GND (Pin 6)    |
| Data      | GPIO4 (Pin 7)  |

## Installation
1. Ensure your Raspberry Pi is up to date:
   ```sh
   sudo apt update && sudo apt upgrade -y
   ```
2. Install the required `Adafruit_DHT` library:
   ```sh
   pip install Adafruit_DHT
   ```

## Usage
1. Connect the DHT11 sensor to the Raspberry Pi as per the wiring instructions.
2. Run the script using:
   ```sh
   python3 dht11_sensor.py
   ```
3. The script will continuously display temperature and humidity readings every 2 seconds.
4. To stop the script, press `Ctrl+C`.

## Code Explanation
```python
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
```

## Troubleshooting
1. **No module named `Adafruit_DHT`**:
   - Ensure the library is installed: `pip install Adafruit_DHT`
   
2. **Failed to retrieve data from the sensor**:
   - Check wiring connections.
   - Ensure correct GPIO pin is specified in the script.
   - Try increasing delay time between readings.
   
3. **Permission Errors**:
   - Try running the script with `sudo`:
     ```sh
     sudo python3 dht11_sensor.py
     ```

## License
This project is open-source and licensed under the MIT License.

## Author
Developed by Araham Abeddin.

