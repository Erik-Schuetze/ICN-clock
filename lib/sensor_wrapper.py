"""
Sensor wrapper module that automatically selects real or mock sensor
based on configuration and platform availability.
"""
import sys
import os

# Add parent directory to path for config import
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from config import MOCK_MODE

# Try to import real sensor, fall back to mock if unavailable
sensor_available = False
use_mock = MOCK_MODE

if not use_mock:
    try:
        from sensirion_i2c_driver import I2cConnection, LinuxI2cTransceiver
        from sensirion_i2c_scd import Scd4xI2cDevice
        sensor_available = True
        print("Using real Sensirion SCD4x sensor")
    except (ImportError, OSError) as e:
        print(f"Real sensor not available: {e}")
        print("Falling back to mock sensor")
        use_mock = True

if use_mock:
    from mock_sensor import (
        MockScd4xDevice as Scd4xI2cDevice,
        MockI2cConnection as I2cConnection,
        MockLinuxI2cTransceiver as LinuxI2cTransceiver
    )
    sensor_available = True
    print("Using mock sensor for testing")

__all__ = ['I2cConnection', 'LinuxI2cTransceiver', 'Scd4xI2cDevice', 'sensor_available']

