#!/bin/bash

# Teleoperate command with USB camera configuration
lerobot-teleoperate \
    --robot.type=so101_follower \
    --robot.port=/dev/ttyACM1 \
    --robot.cameras="{ front: {type: opencv, index_or_path: '/dev/video1', width: 1920, height: 1080, fps: 30, fourcc: 'MJPG'}, c270: {type: opencv, index_or_path: '/dev/video5', width: 640, height: 480, fps: 30}}" \
    --robot.id=f_0 \
    --teleop.type=so101_leader \
    --teleop.port=/dev/ttyACM0 \
    --teleop.id=l_0 \
    --display_data=true