"""
GPS Data Logger using Raspberry Pi and NMEA Parser

Description:
----------------
This Python script reads GPS data from a GPS module connected to the Raspberry Pi's UART serial port.
It parses NMEA sentences (GPGGA & GPRMC) using the `pynmea2` library and extracts useful information 
such as latitude, longitude, time, and date. The extracted data is then converted to JSON format and printed.

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
- `pynmea2` library for parsing NMEA sentences (`pip install pynmea2`)

Usage:
----------------
- Ensure the Raspberry Pi UART serial port is enabled.
- Run the script: `python3 gps_logger.py`
- Press `Ctrl+C` to exit.

"""

import serial
import json
import pynmea2

# Configure the serial port
ser = serial.Serial("/dev/serial0", baudrate=9600, timeout=1)

def parse_gps_data(data, gps_data):
    """
    Parse NMEA data using pynmea2 library.
    Updates the gps_data dictionary with the parsed data.
    """
    try:
        msg = pynmea2.parse(data)
        if isinstance(msg, pynmea2.types.talker.GGA):  # $GPGGA sentence
            if msg.gps_qual:  # Check if GPS fix is available
                gps_data["latitude"] = round(msg.latitude, 6)
                gps_data["longitude"] = round(msg.longitude, 6)
            else:
                gps_data["status"] = "Waiting for GPS fix..."
        elif isinstance(msg, pynmea2.types.talker.RMC):  # $GPRMC sentence
            if msg.status == "A":  # Check if data is valid
                gps_data["time"] = msg.timestamp.strftime("%H:%M:%S") if msg.timestamp else None
                gps_data["date"] = msg.datestamp.strftime("%Y-%m-%d") if msg.datestamp else None
    except pynmea2.ParseError:
        gps_data["error"] = "Invalid NMEA data"

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
