#!/bin/bash
set -e

# Activate venv (required for lerobot-replay)
source /ssd/.venv-lerobot/bin/activate

# For offline testing, set HF_USER manually
HF_USER="${HF_USER:-skpro19}"
echo "HF_USER: $HF_USER"


# Exhaustive list of other parameters that can be passed to lerobot-replay:
#
# Robot Configuration (--robot.*):
# --robot.type=<type>                     Robot type (e.g., so101_follower, so100_follower, bi_so_follower, reachy2, hope_jr, koch_follower, omx_follower, earthrover_mini_plus, unitree_g1)
# --robot.id=<id>                         Unique identifier for the robot instance
# --robot.calibration_dir=<path>          Directory to store calibration files (optional)
# --robot.port=<port>                     Serial port for single-arm robots (e.g., /dev/ttyACM1)
# --robot.disable_torque_on_disconnect=<bool>  Whether to disable torque when disconnecting (default: True for SO robots, False for Reachy2)
# --robot.max_relative_target=<float|dict> Safety limit for relative positional targets (scalar or per-motor dict)
# --robot.use_degrees=<bool>              Use degrees instead of radians for backward compatibility (default: False)
# --robot.ip_address=<address>            IP address for networked robots like Reachy2 (default: "localhost")
# --robot.port=<int>                      Port number for networked robots (default: 50065 for Reachy2)
# --robot.use_external_commands=<bool>    Use external command system instead of direct control (default: False)
# --robot.with_mobile_base=<bool>         Include mobile base joints for Reachy2 (default: True)
# --robot.with_l_arm=<bool>               Include left arm joints for Reachy2 (default: True)
# --robot.with_r_arm=<bool>               Include right arm joints for Reachy2 (default: True)
#
# For bimanual robots (--robot.* for bi_so_follower):
# --robot.left_arm_config.port=<port>     Serial port for left arm
# --robot.left_arm_config.id=<id>         ID for left arm
# --robot.right_arm_config.port=<port>    Serial port for right arm
# --robot.right_arm_config.id=<id>        ID for right arm
#
# Camera Configuration (--robot.cameras.*):
# --robot.cameras.<name>.fps=<int>        Camera frame rate
# --robot.cameras.<name>.width=<int>      Camera resolution width
# --robot.cameras.<name>.height=<int>     Camera resolution height
#
# Dataset Configuration (--dataset.*):
# --dataset.repo_id=<repo_id>             HuggingFace dataset repository ID (e.g., username/dataset_name)
# --dataset.episode=<int>                 Episode number to replay (0-indexed)
# --dataset.root=<path>                   Local root directory for dataset storage (optional)
# --dataset.fps=<int>                     Frames per second limit for replay (default: 30)
#
# General Configuration:
# --play_sounds=<bool>                    Enable vocal synthesis for events (default: True)
# --display_data=<bool>                   Display all cameras and data on screen (default: False)
# --display_ip=<address>                  IP address for remote Rerun server (optional)
# --display_port=<int>                    Port for remote Rerun server (optional)
# --display_compressed_images=<bool>      Whether to display compressed images in Rerun (default: False)

lerobot-replay \
    --robot.type=so101_follower \
    --robot.port=/dev/ttyACM1 \
    --robot.cameras="{ front: { type: opencv, index_or_path: '/dev/video2', width: 1920, height: 1080, fps: 30, fourcc: 'MJPG' }, c270: { type: opencv, index_or_path: '/dev/video4', width: 640, height: 480, fps: 30 } }" \
    --robot.id=f_1 \
    --dataset.repo_id=${HF_USER}/zandu-balm-Feb20-14-07 \
    --dataset.episode=2 \
    --play_sounds=true \
    --display_data=true
