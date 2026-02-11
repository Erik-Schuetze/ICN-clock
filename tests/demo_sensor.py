#!/usr/bin/env python3
"""
Quick demo of the mock sensor functionality
Run this to verify the mock sensor is working without starting the GUI
"""
import os
import sys
import time

# Add parent and lib directories to path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)
sys.path.insert(0, os.path.join(parent_dir, 'lib'))

from sensor_wrapper import I2cConnection, LinuxI2cTransceiver, Scd4xI2cDevice

print("\n" + "="*60)
print("ICN-Clock Mock Sensor Demo")
print("="*60 + "\n")

# Initialize sensor (will use mock if real sensor not available)
try:
    transceiver = LinuxI2cTransceiver("/dev/i2c-1")
    i2c = I2cConnection(transceiver)
    scd4x = Scd4xI2cDevice(i2c)

    scd4x.stop_periodic_measurement()
    scd4x.reinit()
    print("Initializing sensor...")
    time.sleep(1)

    scd4x.start_periodic_measurement()
    print("Starting measurements...\n")
    time.sleep(1)

    # Read and display 5 measurements
    for i in range(5):
        co2, temp, rh = scd4x.read_measurement()
        print(f"Reading {i+1}:")
        print(f"  Temperature: {temp.degrees_celsius:.1f}°C")
        print(f"  Humidity:    {rh.percent_rh:.1f}%")
        print(f"  CO2:         {co2.co2} ppm")
        print()
        time.sleep(2)

    print("="*60)
    print("Demo complete! Mock sensor is working correctly.")
    print("="*60 + "\n")

except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()

