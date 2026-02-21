#!/bin/bash

# For offline testing, set HF_USER manually
HF_USER="${HF_USER:-skpro19}"
echo "HF_USER: $HF_USER"

lerobot-record \
  --robot.type=so101_follower \
  --robot.port=/dev/ttyACM1 \
  --robot.cameras="{ front: { type: opencv, index_or_path: '/dev/video2', width: 1920, height: 1080, fps: 30, fourcc: 'MJPG' }, c270: { type: opencv, index_or_path: '/dev/video4', width: 640, height: 480, fps: 30 } }" \
  --robot.id=f_1 \
  --display_data=true \
  --dataset.repo_id=${HF_USER}/eval_act_zandu-balm-$(date +%Y%m%d-%H%M%S) \
  --dataset.push_to_hub=false \
  --dataset.single_task="Grab the item and put it in the bowl" \
  --dataset.reset_time_s=20 \
  --dataset.episode_time_s=1000 \
  --policy.path=${HF_USER}/act_zandu-balm-Feb20-14-07 \
  --policy.device=cuda \
  --teleop.type=so101_leader \
  --teleop.port=/dev/ttyACM0 \
  --teleop.id=l_1 