"""
Mock sensor module for testing on non-Raspberry Pi systems.
Provides realistic sensor data simulation without requiring actual hardware.
"""
import random
import time
from typing import Tuple


class MockTemperature:
    """Mock temperature reading"""
    def __init__(self, celsius: float):
        self.degrees_celsius = celsius


class MockHumidity:
    """Mock humidity reading"""
    def __init__(self, percent: float):
        self.percent_rh = percent


class MockCO2:
    """Mock CO2 reading"""
    def __init__(self, ppm: int):
        self.co2 = ppm


class MockScd4xDevice:
    """
    Mock Sensirion SCD4x sensor device.
    Simulates realistic environmental readings with slight variations.
    """

    def __init__(self, i2c_connection=None):
        # Base values for simulation
        self.base_temp = 22.0  # Base temperature in Celsius
        self.base_humidity = 45.0  # Base humidity percentage
        self.base_co2 = 800  # Base CO2 in ppm

        # Variation ranges
        self.temp_variation = 3.0
        self.humidity_variation = 10.0
        self.co2_variation = 200

        # Current values (will vary over time)
        self.current_temp = self.base_temp
        self.current_humidity = self.base_humidity
        self.current_co2 = self.base_co2

        print("Mock SCD4x sensor initialized")

    def stop_periodic_measurement(self):
        """Mock stop measurement - does nothing"""
        pass

    def reinit(self):
        """Mock reinit - does nothing"""
        pass

    def start_periodic_measurement(self):
        """Mock start measurement - does nothing"""
        print("Mock sensor: Started periodic measurement")

    def read_measurement(self) -> Tuple[MockCO2, MockTemperature, MockHumidity]:
        """
        Simulate sensor readings with realistic variations.
        Returns (co2, temperature, humidity) tuple.
        """
        # Add small random variations to simulate realistic sensor behavior
        temp_delta = random.uniform(-0.5, 0.5)
        humidity_delta = random.uniform(-2, 2)
        co2_delta = random.randint(-50, 50)

        # Update current values with damping to prevent wild swings
        self.current_temp += temp_delta * 0.3
        self.current_humidity += humidity_delta * 0.3
        self.current_co2 += co2_delta * 0.3

        # Keep values within realistic bounds
        self.current_temp = max(18, min(28, self.current_temp))
        self.current_humidity = max(30, min(70, self.current_humidity))
        self.current_co2 = max(400, min(1500, self.current_co2))

        # Create mock reading objects
        co2_reading = MockCO2(int(self.current_co2))
        temp_reading = MockTemperature(self.current_temp)
        humidity_reading = MockHumidity(self.current_humidity)

        return co2_reading, temp_reading, humidity_reading


class MockI2cConnection:
    """Mock I2C connection - does nothing"""
    def __init__(self, transceiver):
        pass


class MockLinuxI2cTransceiver:
    """Mock I2C transceiver - does nothing"""
    def __init__(self, device_path: str):
        self.device_path = device_path


