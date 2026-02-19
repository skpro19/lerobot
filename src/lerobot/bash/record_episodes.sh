# For offline testing, set HF_USER manually
HF_USER="skpro19"
echo "HF_USER: $HF_USER"

lerobot-record \
    --robot.type=so101_follower \
    --robot.port=/dev/ttyACM1 \
    --robot.cameras="{ front: {type: opencv, index_or_path: '/dev/video1', width: 1920, height: 1080, fps: 30, fourcc: 'MJPG'}, c270: {type: opencv, index_or_path: '/dev/video5', width: 640, height: 480, fps: 30}}" \
    --robot.id=f_0 \
    --teleop.type=so101_leader \
    --teleop.port=/dev/ttyACM0 \
    --teleop.id=l_0 \
    --display_data=true \
    --dataset.repo_id="$HF_USER/record-test-5" \
    --dataset.push_to_hub=false \
    --dataset.num_episodes=5 \
    --dataset.single_task="Grab Zandu [1]"