"""
GPS Data Logger using Raspberry Pi and NMEA Parsing (Without pynmea2 Library)

Description:
----------------
This Python script reads GPS data from a GPS module connected to the Raspberry Pi's UART serial port.
It manually parses NMEA sentences ($GPGGA & $GPRMC) to extract latitude, longitude, time, and date.
The extracted data is then converted to JSON format and printed.

Wiring:
----------------
- GPS Module TX → Raspberry Pi GPIO 15 (RX) (Physical Pin 10)
- GPS Module RX → Raspberry Pi GPIO 14 (TX) (Physical Pin 8)
- GPS Module GND → Raspberry Pi GND (Any GND pin)
- GPS Module VCC → Raspberry Pi 3.3V or 5V (Check module specs)

Dependencies:
----------------
- Python 3.x
- `pyserial` library for serial communication (`pip install pyserial`)

Usage:
----------------
- Ensure the Raspberry Pi UART serial port is enabled.
- Run the script: `python3 gps_logger.py`
- Press `Ctrl+C` to exit.

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
                # Convert dictionary to stringified JSON
                json_string = json.dumps(gps_data)
                print(json_string)  # Print stringified JSON

except KeyboardInterrupt:
    print("Exiting program")
    ser.close()
