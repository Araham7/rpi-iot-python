# Enabling UART on Raspberry Pi

## Overview
This guide explains how to enable the **UART (Serial) protocol** on a Raspberry Pi to communicate with devices like the **NEO-6M GPS module**.

## Steps to Enable UART

### 1. Update and Upgrade System
```bash
sudo apt update && sudo apt upgrade -y
```

### 2. Enable UART Using raspi-config
Run the Raspberry Pi configuration tool:
```bash
sudo raspi-config
```
Navigate to:
```
Interfacing Options > Serial Port
```
- Select **No** when asked if you want a login shell over serial.
- Select **Yes** to enable the serial port hardware.
- Exit and reboot:
```bash
sudo reboot
```

### 3. Verify UART Configuration
After reboot, check available serial ports:
```bash
ls -l /dev/serial*
```
The UART interface should be available as **`/dev/serial0`** or **`/dev/ttyS0`**.

To test, connect a device (e.g., NEO-6M GPS) and use `minicom` or `screen`:
```bash
sudo apt install minicom -y
minicom -b 9600 -o -D /dev/serial0
```

## Notes
- If using a Raspberry Pi 3/4/5, **`/dev/serial0`** maps to the **PL011 UART**.
- For higher stability, consider disabling Bluetooth (`dtoverlay=disable-bt` in `config.txt`).

## Troubleshooting
- Run `dmesg | grep tty` to check for serial errors.
- Ensure proper wiring for RX/TX connections.
- Use `raspi-gpio get` to verify pin configurations.

