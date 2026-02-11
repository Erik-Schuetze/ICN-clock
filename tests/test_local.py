#!/usr/bin/env python3
"""
Local testing script for ICN-clock
Runs the clock with mock sensor data for testing on any PC/Mac
"""
import os
import sys

# Change to parent directory (project root)
script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(script_dir)
os.chdir(parent_dir)

# Add parent directory to Python path so we can import main
sys.path.insert(0, parent_dir)

# Use local config for testing
config_backup = False
local_config = os.path.join(script_dir, 'config.local.py')
if os.path.exists(local_config):
    # Rename current config temporarily
    if os.path.exists('config.py'):
        if os.path.exists('config.py.bak'):
            os.remove('config.py.bak')
        os.rename('config.py', 'config.py.bak')
        config_backup = True

    # Copy local config to config.py
    import shutil
    shutil.copy(local_config, 'config.py')

    print("=" * 60)
    print("Running in LOCAL TEST MODE")
    print("Using mock sensor data")
    print("=" * 60)
    print()

try:
    # Import and run main
    import main
except KeyboardInterrupt:
    print("\nTest stopped by user")
except Exception as e:
    print(f"\nError running test: {e}")
    import traceback
    traceback.print_exc()
finally:
    # Restore original config
    if config_backup:
        if os.path.exists('config.py'):
            os.remove('config.py')
        os.rename('config.py.bak', 'config.py')
        print("\nOriginal config restored")


