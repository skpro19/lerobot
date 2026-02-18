# Copyright 2024 The HuggingFace Inc. team. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Script to check calibration values for teleoperators and robots.

This script shows both stored calibration values and motor calibration values.

Example:

```shell
# Check stored calibration only
python check_calibration.py --teleop_id=l_0
python check_calibration.py --robot_id=f_0

# Check both stored calibration and motor calibration values
python check_calibration.py --teleop.type=so101_leader --teleop.port=/dev/ttyACM1 --teleop.id=l_0
python check_calibration.py --robot.type=so101_follower --robot.port=/dev/ttyACM0 --robot.id=f_0
```
"""

import json
import logging
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Optional

import draccus

from lerobot.motors.motors_bus import MotorCalibration
from lerobot.utils.constants import HF_LEROBOT_CALIBRATION, ROBOTS, TELEOPERATORS
from lerobot.utils.utils import init_logging
from lerobot.robots import RobotConfig, make_robot_from_config, so_follower  # noqa: F401
from lerobot.teleoperators import TeleoperatorConfig, make_teleoperator_from_config, so_leader  # noqa: F401


@dataclass
class CheckCalibrationConfig:
    # Teleoperator configuration (optional, for reading current motor values)
    teleop: Optional[TeleoperatorConfig] = None
    # Robot configuration (optional, for reading current motor values)
    robot: Optional[RobotConfig] = None
    # Teleoperator ID to check stored calibration for (can be separate from teleop config)
    teleop_id: Optional[str] = None
    # Robot ID to check stored calibration for (can be separate from robot config)
    robot_id: Optional[str] = None

    def __post_init__(self):
        # Must specify either stored calibration IDs or device configs (or both)
        has_stored = self.teleop_id or self.robot_id
        has_devices = self.teleop or self.robot

        if not has_stored and not has_devices:
            raise ValueError("Must specify either stored calibration IDs (--teleop_id/--robot_id) or device configs (--teleop.* / --robot.*) or both")

        # If device configs provided, extract IDs for stored calibration lookup
        if self.teleop and not self.teleop_id:
            self.teleop_id = self.teleop.id
        if self.robot and not self.robot_id:
            self.robot_id = self.robot.id


def print_calibration_table(device_type: str, device_id: str, calibration: Dict[str, MotorCalibration], motor_calibration_values: Optional[Dict[str, Dict]] = None):
    """Print calibration data in separate tables for stored values and motor-stored values."""
    if not calibration:
        print(f"\n{device_type.upper()} CALIBRATION - ID: {device_id}")
        print("=" * 80)
        print("No calibration data found.")
        print("=" * 80)
        return

    # First table: Stored Calibration Values
    print(f"\n{device_type.upper()} STORED CALIBRATION VALUES - ID: {device_id}")
    print("=" * 80)
    print(f"{'Motor':<15} {'ID':<3} {'Drive Mode':<10} {'Homing Offset':<13} {'Range Min':<10} {'Range Max':<10}")
    print("-" * 80)

    for motor_name, motor_cal in calibration.items():
        print(f"{motor_name:<15} {motor_cal.id:<3} {motor_cal.drive_mode:<10} {motor_cal.homing_offset:<13} {motor_cal.range_min:<10} {motor_cal.range_max:<10}")

    print("=" * 80)

    # Second table: Motor Calibration Values (if available)
    if motor_calibration_values:
        print(f"\n{device_type.upper()} MOTOR CALIBRATION VALUES - ID: {device_id}")
        print("=" * 80)
        print(f"{'Motor':<15} {'ID':<3} {'Drive Mode':<10} {'Homing Offset':<13} {'Range Min':<10} {'Range Max':<10}")
        print("-" * 80)

        for motor_name in calibration.keys():
            motor_vals = motor_calibration_values.get(motor_name)
            if motor_vals:
                print(f"{motor_name:<15} {motor_vals.get('id', 'N/A'):<3} {motor_vals.get('drive_mode', 'N/A'):<10} {motor_vals.get('homing_offset', 'N/A'):<13} {motor_vals.get('range_min', 'N/A'):<10} {motor_vals.get('range_max', 'N/A'):<10}")
            else:
                print(f"{motor_name:<15} {'N/A':<3} {'N/A':<10} {'N/A':<13} {'N/A':<10} {'N/A':<10}")

        print("=" * 80)


def check_port_accessibility(port: str) -> None:
    """Check if a port is accessible and raise an error with helpful message if not."""
    port_path = Path(port)
    
    if not port_path.exists():
        raise FileNotFoundError(
            f"Port {port} does not exist.\n"
            f"Please check that the device is connected and the port path is correct."
        )
    
    if not os.access(port, os.R_OK | os.W_OK):
        # Try to determine the actual port name (might be ttyACM0, ttyUSB0, etc.)
        port_name = port_path.name
        raise PermissionError(
            f"Port {port} is not accessible (permission denied).\n"
            f"To fix this, run:\n"
            f"  sudo chmod 666 {port}\n"
            f"Or add your user to the dialout group:\n"
            f"  sudo usermod -a -G dialout $USER\n"
            f"(Then log out and log back in for the group change to take effect)"
        )


def read_motor_calibration_values(device):
    """Read calibration values stored in the motors themselves."""
    try:
        motor_calibrations = {}
        for motor_name, motor in device.bus.motors.items():
            try:
                # Read calibration values from the motor
                homing_offset = device.bus.read("Homing_Offset", motor_name)
                range_min = device.bus.read("Min_Position_Limit", motor_name)
                range_max = device.bus.read("Max_Position_Limit", motor_name)

                motor_calibrations[motor_name] = {
                    'id': motor.id,
                    'drive_mode': 0,  # Usually 0 for servo motors
                    'homing_offset': homing_offset,
                    'range_min': range_min,
                    'range_max': range_max
                }
            except Exception as e:
                logging.warning(f"Could not read calibration for motor {motor_name}: {e}")
                motor_calibrations[motor_name] = None

        return motor_calibrations
    except Exception as e:
        logging.warning(f"Could not read motor calibration values: {e}")
        return None


def check_device_calibration(device_type: str, device_name: str, device_id: str, device=None):
    """Check and display calibration for a specific device."""
    if device_type == "teleop":
        calibration_dir = HF_LEROBOT_CALIBRATION / TELEOPERATORS / device_name
    elif device_type == "robot":
        calibration_dir = HF_LEROBOT_CALIBRATION / ROBOTS / device_name
    else:
        raise ValueError(f"Unknown device type: {device_type}")

    calibration_fpath = calibration_dir / f"{device_id}.json"

    if not calibration_fpath.exists():
        print(f"\n{device_type.upper()} CALIBRATION - ID: {device_id}")
        print("=" * 120)
        print(f"No calibration file found at: {calibration_fpath}")
        print("=" * 120)
        return

    try:
        # Load calibration data
        with open(calibration_fpath) as f, draccus.config_type("json"):
            calibration: Dict[str, MotorCalibration] = draccus.load(dict[str, MotorCalibration], f)

        # Read motor calibration values if device is connected
        motor_calibration_values = None
        if device:
            motor_calibration_values = read_motor_calibration_values(device)

        print_calibration_table(device_type, device_id, calibration, motor_calibration_values)

    except Exception as e:
        print(f"\nError loading calibration for {device_type} {device_id}: {e}")
        print("=" * 120)


@draccus.wrap()
def check_calibration(cfg: CheckCalibrationConfig):
    init_logging()
    logging.info(f"Checking calibration for teleop_id={cfg.teleop_id}, robot_id={cfg.robot_id}")

    teleop_device = None
    robot_device = None

    try:
        # Connect to teleoperator if config provided
        if cfg.teleop:
            if cfg.teleop.port:
                check_port_accessibility(cfg.teleop.port)
            teleop_device = make_teleoperator_from_config(cfg.teleop)
            teleop_device.connect(calibrate=False)
            logging.info(f"Connected to teleoperator {cfg.teleop.id}")

        # Connect to robot if config provided
        if cfg.robot:
            if cfg.robot.port:
                check_port_accessibility(cfg.robot.port)
            robot_device = make_robot_from_config(cfg.robot)
            robot_device.connect(calibrate=False)
            logging.info(f"Connected to robot {cfg.robot.id}")

        # Check teleoperator calibration
        if cfg.teleop_id:
            check_device_calibration("teleop", "so_leader", cfg.teleop_id, teleop_device)

        # Check robot calibration
        if cfg.robot_id:
            check_device_calibration("robot", "so_follower", cfg.robot_id, robot_device)

    finally:
        # Clean up connections
        if teleop_device:
            try:
                teleop_device.disconnect()
                logging.info("Disconnected from teleoperator")
            except Exception as e:
                logging.warning(f"Error disconnecting teleoperator: {e}")

        if robot_device:
            try:
                robot_device.disconnect()
                logging.info("Disconnected from robot")
            except Exception as e:
                logging.warning(f"Error disconnecting robot: {e}")


def main():
    check_calibration()


if __name__ == "__main__":
    main()
