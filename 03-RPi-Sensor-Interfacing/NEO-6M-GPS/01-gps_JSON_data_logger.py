"""
GPS NMEA Data Parser Script

This program reads and parses NMEA data from a GPS module connected to a Raspberry Pi via a serial interface. It demonstrates how to:
1. Initialize a serial connection to the GPS module.
2. Parse NMEA sentences (GPGGA and GPRMC) to extract latitude, longitude, date, and time.
3. Store the parsed data in a dictionary and output it in JSON format.

Steps:
1. Configures the serial port (`/dev/serial0`) with a baud rate of 9600 and a timeout of 1 second.
2. Defines a `parse_gps_data` function to:
   - Parse GPGGA sentences to extract latitude and longitude.
   - Parse GPRMC sentences to extract date and time.
   - Update a dictionary (`gps_data`) with the parsed data.
3. Continuously reads data from the serial port, parses it, and prints the parsed data in JSON format.
4. Handles a KeyboardInterrupt (Ctrl+C) to gracefully close the serial connection and exit the program.

Dependencies:
- serial (for serial communication)
- json (for JSON output)

Hardware Requirements:
- GPS module with NMEA output (e.g., NEO-6M, NEO-7M).
- Raspberry Pi with UART enabled.

Wiring:
- GPS TX → Raspberry Pi RX (GPIO15, Pin 10)
- GPS RX → Raspberry Pi TX (GPIO14, Pin 8)
- GPS VCC → 3.3V or 5V (depending on the module)
- GPS GND → GND

Usage:
1. Connect the GPS module to the Raspberry Pi as per the wiring instructions.
2. Run the script, and the program will continuously read and parse NMEA data from the GPS module.
3. The parsed data (latitude, longitude, date, and time) will be printed in JSON format.
4. The program will continue running until interrupted (e.g., by pressing Ctrl+C).

Author: Araham Abeddin.
"""

import serial
import json

# Configure the serial port
ser = serial.Serial("/dev/serial0", baudrate=9600, timeout=1)

def parse_gps_data(data, gps_data):
    """
    Parse NMEA data to extract latitude, longitude, date, and time.
    Updates the gps_data dictionary with the parsed data.
    """
    if data.startswith("$GPGGA"):
        # Parse latitude and longitude
        parts = data.split(",")
        if parts[6] != "0":  # Check if GPS fix is available
            try:
                lat = float(parts[2][:2]) + float(parts[2][2:]) / 60
                lon = float(parts[4][:3]) + float(parts[4][3:]) / 60
                if parts[3] == "S":
                    lat = -lat
                if parts[5] == "W":
                    lon = -lon
                gps_data["latitude"] = round(lat, 6)
                gps_data["longitude"] = round(lon, 6)
            except ValueError:
                gps_data["error"] = "Invalid GPS data"
        else:
            gps_data["status"] = "Waiting for GPS fix..."

    elif data.startswith("$GPRMC"):
        # Parse date and time
        parts = data.split(",")
        if parts[2] == "A":  # Check if data is valid
            try:
                # Extract time (HHMMSS.SSS format)
                gps_time = parts[1]
                if gps_time:
                    hours = gps_time[:2]
                    minutes = gps_time[2:4]
                    seconds = gps_time[4:6]
                    gps_data["time"] = f"{hours}:{minutes}:{seconds}"

                # Extract date (DDMMYY format)
                gps_date = parts[9]
                if gps_date:
                    day = gps_date[:2]
                    month = gps_date[2:4]
                    year = gps_date[4:6]
                    gps_data["date"] = f"20{year}-{month}-{day}"  # Assuming 21st century
            except ValueError:
                gps_data["error"] = "Invalid date/time data"
        else:
            gps_data["status"] = "Invalid GPS data"

try:
    gps_data = {}  # Dictionary to store all GPS data
    while True:
        data = ser.readline().decode("utf-8").strip()
        if data:
            parse_gps_data(data, gps_data)  # Update the dictionary with new data
            if gps_data:  # If data is not empty
                print(json.dumps(gps_data, indent=4))  # Print JSON output

except KeyboardInterrupt:
    print("Exiting program")
    ser.close()
