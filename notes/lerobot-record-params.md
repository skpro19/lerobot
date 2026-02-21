# LeRobot Record Parameters

This document lists all parameters that can be passed to the `lerobot-record` command, organized by category.

## Dataset Configuration (`--dataset.*`)

Parameters related to dataset creation, storage, and encoding:

- `repo_id` (required): Dataset identifier in format `{hf_username}/{dataset_name}` (e.g., `lerobot/test`)
- `single_task` (required): Short description of the task being performed
- `root`: Root directory for dataset storage
- `fps`: Frames per second (default: 30)
- `episode_time_s`: Recording duration per episode in seconds (default: 60)
- `reset_time_s`: Environment reset time between episodes in seconds (default: 60)
- `num_episodes`: Total number of episodes to record (default: 50)
- `video`: Whether to encode frames into video (default: true)
- `push_to_hub`: Upload dataset to Hugging Face Hub (default: true)
- `private`: Upload as private repository (default: false)
- `tags`: List of tags for the dataset
- `num_image_writer_processes`: Number of subprocesses for frame saving (default: 0)
- `num_image_writer_threads_per_camera`: Threads per camera for frame writing (default: 4)
- `video_encoding_batch_size`: Episodes to record before batch encoding (default: 1)
- `vcodec`: Video codec for encoding (`h264`, `hevc`, `libsvtav1`; default: `libsvtav1`)
- `rename_map`: Dictionary to rename observation/action keys

## Robot Configuration (`--robot.*`)

Parameters for the robot being recorded:

- `type` (required): Robot type (e.g., `so100_follower`, `so101_follower`, `bi_so_follower`, `reachy2`, `unitree_g1`, `earthrover_mini_plus`, `hope_jr_arm`, `hope_jr_hand`, `koch_follower`, `omx_follower`, `lekiwi`, `lekiwi_client`, etc.)
- `id`: Identifier to distinguish between robots of same type
- `calibration_dir`: Directory for calibration files
- `port`: Serial port for robot connection (robot-specific; SO arms)
- `disable_torque_on_disconnect`: Disable torque when disconnecting (default: true)
- `max_relative_target`: Safety limit for relative positional targets (scalar or dict)
- `cameras`: Dictionary of camera configurations (see Camera Configuration below)
- `use_degrees`: Use degrees instead of radians (default: false)

### Bimanual robot (`bi_so_follower`)
- `left_arm_config.port`, `left_arm_config.cameras`, `left_arm_config.disable_torque_on_disconnect`, `left_arm_config.max_relative_target`, `left_arm_config.use_degrees`
- `right_arm_config.port`, `right_arm_config.cameras`, etc. (same structure)

## Teleoperator Configuration (`--teleop.*`)

Parameters for teleoperation control (optional). At least one of `teleop` or `policy` must be set.

- `type`: Teleoperator type (e.g., `so100_leader`, `so101_leader`, `bi_so_leader`, `keyboard`, `keyboard_ee`, `keyboard_rover`, `gamepad`, `phone`, `omx_leader`, `reachy2_teleoperator`, `koch_leader`, `homunculus_glove`, `homunculus_arm`, etc.)
- `id`: Identifier to distinguish between teleoperators
- `calibration_dir`: Directory for calibration files
- `port`: Serial port for teleoperator connection (device-specific; SO leaders)
- `use_degrees`: Use degrees instead of radians (default: false)

### Bimanual teleop (`bi_so_leader`)
- `left_arm_config.port`, `left_arm_config.use_degrees`
- `right_arm_config.port`, `right_arm_config.use_degrees`

## Policy Configuration (`--policy.*`)

Parameters for policy-based control (optional). When set, the robot can be controlled by the policy (e.g. for evaluation/inference). At least one of `teleop` or `policy` must be set.

- `path` (required if using policy): Path or HuggingFace repo ID for pretrained policy; config is loaded from here and CLI overrides apply
- `type`: Policy type (inferred from loaded config when using `path`)
- `n_obs_steps`: Number of observation steps for policy input (default: 1)
- `input_features`: Dictionary defining input data shapes
- `output_features`: Dictionary defining output data shapes
- `device`: Compute device (`cuda`, `cpu`, `mps`, etc.)
- `use_amp`: Use Automatic Mixed Precision (default: false)
- `use_peft`: Whether policy uses PEFT (default: false)
- `push_to_hub`: Upload policy to Hub (default: true)
- `repo_id`: Policy repository ID
- `private`: Upload as private repository
- `tags`: List of tags for the policy
- `license`: License for the policy

## Camera Configuration (`--robot.cameras.*` or `--robot.left_arm_config.cameras.*` / `--robot.right_arm_config.cameras.*`)

Parameters for individual cameras within robot configuration. Base fields for all camera types:

- `type`: Camera type (`opencv`, `intelrealsense`, `zmq`, `reachy2_camera`)
- `fps`: Frames per second (required)
- `width`: Frame width in pixels (required)
- `height`: Frame height in pixels (required)

### OpenCV Camera (`opencv`):
- `index_or_path`: Camera device index (int) or video file path (str)
- `color_mode`: Color output mode (`rgb` or `bgr`; default: `rgb`)
- `rotation`: Image rotation (0, 90, 180, 270 degrees; default: 0)
- `warmup_s`: Warmup time in seconds before returning from connect (default: 1)
- `fourcc`: FOURCC video format code (e.g., "MJPG", "YUYV"; 4-character string)

### Intel RealSense Camera (`intelrealsense`):
- `serial_number_or_name`: Camera serial number or human-readable name
- `color_mode`: Color output mode (`rgb` or `bgr`; default: `rgb`)
- `use_depth`: Enable depth stream (default: false)
- `rotation`: Image rotation (0, 90, 180, 270 degrees; default: 0)
- `warmup_s`: Warmup time in seconds (default: 1)

### ZMQ Camera (`zmq`):
- `server_address`: ZMQ server address (required)
- `port`: ZMQ port (default: 5555)
- `camera_name`: Camera name (default: "zmq_camera")
- `color_mode`: Color output mode (`rgb` or `bgr`; default: `rgb`)
- `timeout_ms`: Timeout in milliseconds (default: 5000)

### Reachy 2 Camera (`reachy2_camera`):
- `name`: Device name (`teleop` or `depth`)
- `image_type`: For teleop: `left` or `right`; for depth: `rgb` or `depth`
- `color_mode`: Color output mode (`rgb` or `bgr`; default: `rgb`)
- `ip_address`: Robot IP (default: "localhost")
- `port`: Camera server port (default: 50065)

## Display and control (top-level)

Parameters for visualization and recording behavior. Pass as `--display_data=true`, `--resume=false`, etc.:

- `display_data`: Display cameras on screen (default: false)
- `display_ip`: IP address for remote Rerun server
- `display_port`: Port for remote Rerun server
- `display_compressed_images`: Display compressed images in Rerun (default: false)
- `play_sounds`: Use vocal synthesis for events (default: true)
- `resume`: Resume recording on existing dataset (default: false)

## Plugin and extension

- `env.discover_packages_path`: Python package path to discover third-party plugins (e.g. custom robots/teleops/cameras). The CLI strips this arg and loads the plugin before parsing; it is not a field on the record config.

## Usage Notes

The parameters are passed using dot notation (e.g., `--robot.type=so100_follower`, `--dataset.num_episodes=10`, `--robot.cameras.laptop.type=opencv`). Complex nested structures like camera configurations use JSON strings (e.g. `--robot.cameras='{ front: { type: opencv, ... } }'`). When using `--policy.path=<repo_or_dir>`, the policy config is loaded from that path and any `--policy.<key>=<value>` overrides apply. You must specify either a teleoperator, a policy, or both.

Example usage:
```bash
lerobot-record \
    --robot.type=so100_follower \
    --robot.port=/dev/tty.usbmodem58760431541 \
    --robot.cameras="{laptop: {type: opencv, index_or_path: 0, width: 640, height: 480, fps: 30}}" \
    --robot.id=black \
    --dataset.repo_id=<my_username>/<my_dataset_name> \
    --dataset.num_episodes=2 \
    --dataset.single_task="Grab the cube"
```