# HC-SR04 Ultrasonic Distance Sensor with Raspberry Pi

## Overview
This project demonstrates how to measure distance using an **HC-SR04 ultrasonic sensor** connected to a **Raspberry Pi**. The script initializes the GPIO pins, sends a trigger pulse to the sensor, measures the echo pulse duration, and calculates the distance based on the speed of sound.

## Features
- Initializes the **GPIO pins** for the HC-SR04 sensor.
- Sends a **10-microsecond trigger pulse** to the sensor.
- Measures the **duration of the echo pulse**.
- Calculates the **distance in centimeters**.
- Continuously measures and displays the distance.
- Handles **KeyboardInterrupt** (Ctrl+C) for safe GPIO cleanup.

## Hardware Requirements
- **Raspberry Pi** (any model with GPIO support)
- **HC-SR04 Ultrasonic Sensor**
- **Voltage divider circuit** (to step down Echo pin voltage from 5V to 3.3V)
- **Jumper wires**

## Wiring Instructions
Connect the HC-SR04 sensor to the Raspberry Pi as follows:

| HC-SR04 Pin | Raspberry Pi Pin |
|------------|----------------|
| VCC        | 5V (Pin 2 or 4) |
| GND        | GND (Pin 6 or 9) |
| Trig       | GPIO23 (Pin 16) |
| Echo       | Voltage Divider → GPIO12 (Pin 32) |

⚠️ **Important:** The Echo pin outputs **5V**, while the Raspberry Pi GPIO operates at **3.3V**. Use a **voltage divider** (with resistors, e.g., 1kΩ and 2kΩ) to step down the voltage.

## Dependencies
Ensure you have the required libraries installed before running the script:
```sh
pip install RPi.GPIO
```

## Code Explanation
### 1. GPIO Setup
- **BCM mode** is used for GPIO numbering.
- **Trig pin (GPIO23)** is set as an output.
- **Echo pin (GPIO12)** is set as an input.

### 2. `get_distance()` Function
- Sends a **10-microsecond pulse** to the Trig pin to trigger the sensor.
- Measures the **time taken** for the echo to return.
- Uses the **speed of sound (343 m/s or 17150 cm/s)** to calculate the distance.
- Returns the distance in **centimeters**.

### 3. Continuous Measurement Loop
- Calls `get_distance()` every **1 second**.
- Displays the measured distance in **cm**.
- Handles **Ctrl+C** to stop the script and clean up the GPIO.

## Usage
1. **Connect the HC-SR04 sensor** to the Raspberry Pi following the wiring diagram.
2. **Run the script** using:
   ```sh
   python3 hc_sr04.py
   ```
3. The program will continuously **print the distance** in centimeters.
4. To stop the program, press **Ctrl+C**.

## Expected Output
```sh
Distance: 15.3 cm
Distance: 14.8 cm
Distance: 15.1 cm
Measurement stopped by user
```

## Full Code
```python
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
```

## Troubleshooting
### 1. **No Output or Constant Zero Distance**
- Ensure the **Trig and Echo pins** are correctly connected.
- Check the **voltage divider** on the Echo pin.

### 2. **Incorrect or Fluctuating Readings**
- Ensure the **sensor is stable** and not moving.
- Remove obstacles that might cause **interference**.
- Avoid running in **noisy electrical environments**.

## References
- [HC-SR04 Datasheet](https://cdn.sparkfun.com/datasheets/Sensors/Proximity/HCSR04.pdf)
- [Raspberry Pi GPIO Documentation](https://www.raspberrypi.org/documentation/usage/gpio/)

## License
This project is **open-source** and licensed under the MIT License.

