"""Test DEBUG_PRINT flag functionality"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Test with DEBUG_PRINT = True
print("=" * 50)
print("Test 1: DEBUG_PRINT = True")
print("=" * 50)

DEBUG_PRINT = True

def debug_print(*args, **kwargs):
    """Print only if DEBUG_PRINT is enabled"""
    if DEBUG_PRINT:
        print(*args, **kwargs)

debug_print("This message SHOULD be visible")
debug_print(f"Weather updated: 15°C, code: 61")
debug_print(f"Sunrise: 6:00, Sunset: 22:00")

print("\n" + "=" * 50)
print("Test 2: DEBUG_PRINT = False")
print("=" * 50)

DEBUG_PRINT = False

debug_print("This message should NOT be visible")
debug_print(f"Weather updated: 15°C, code: 61")
debug_print(f"Sunrise: 6:00, Sunset: 22:00")

print("\n" + "=" * 50)
print("Test Complete!")
print("=" * 50)
print("When DEBUG_PRINT = False, debug messages are suppressed")
print("When DEBUG_PRINT = True, debug messages are displayed")

