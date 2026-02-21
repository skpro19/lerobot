---
name: fix-robot-cameras
description: Configures a given shell script to use the ARC (USB2.0_CAM1) and Logitech C270 robot cameras with correct device paths and resolutions. Use when fixing or setting up camera configuration in a .sh file, when the user mentions robot cameras, ARC, C270, or teleoperate/record scripts.
---

# Fix Robot Cameras

Ensures a provided `.sh` file uses the correct `--robot.cameras` configuration for the ARC camera (USB2.0_CAM1) and the Logitech C270, and that both cameras are connected.

## When to Use

- User provides or points to a `.sh` file and wants camera configuration fixed or set up.
- User mentions ARC and C270 cameras, robot cameras, or teleoperate/record scripts in the context of camera setup.

## Input

- A single `.sh` file path. If the user does not specify a file, ask which script to update.

## Workflow

Follow these steps in order.

### Step 1: List attached cameras and supported resolutions

Run these commands and keep the output for the next steps:

```bash
v4l2-ctl --list-devices
```

For each Video Capture device listed (e.g. `/dev/video0`, `/dev/video2`, `/dev/video4`), run:

```bash
v4l2-ctl -d /dev/videoX --list-formats-ext
```

(Replace `/dev/videoX` with the actual device path.) Use the output to identify which device corresponds to which camera and which resolutions/framerates are supported.

### Step 2: Verify both required cameras are connected

From the Step 1 output, confirm:

- **USB2.0_CAM1 (ARC)** is present. It may appear as "USB2.0_CAM1" or "ARC International Camera" and is typically on `/dev/video2` (or the next available capture node for that device).
- **Logitech C270** is present. It may appear as "C270 HD WEBCAM" or "Logitech" and is typically on `/dev/video4` (or the next available capture node for that device).

If either camera is missing, do not edit the script. Report which camera is missing and ask the user to connect it, then re-run from Step 1.

### Step 3: Ensure the script uses `--robot.cameras`

Open the given `.sh` file and look for a `--robot.cameras` argument (e.g. on the same line as `lerobot-teleoperate`, `lerobot-record`, or similar).

- If `--robot.cameras` is missing: tell the user and do not make any changes to the script.
- If `--robot.cameras` is present: proceed to update its value so it includes the `front` and `c270` keys as in Steps 4 and 5.

### Step 4: Set the `front` key to the ARC camera parameters

Set the `front` key inside `--robot.cameras` to the ARC (USB2.0_CAM1) configuration. Use the device path that corresponds to USB2.0_CAM1 from Step 1 (often `/dev/video2`).

**Exact value for `front`:**

```
front: { type: opencv, index_or_path: '/dev/video2', width: 1920, height: 1080, fps: 30, fourcc: 'MJPG' }
```

If Step 1 showed USB2.0_CAM1 on a different device (e.g. `/dev/video3`), use that path in `index_or_path` instead of `/dev/video2`.

### Step 5: Set the `c270` key to the Logitech C270 parameters

Set the `c270` key inside `--robot.cameras` to the Logitech C270 configuration. Use the device path that corresponds to the C270 from Step 1 (often `/dev/video4`).

**Exact value for `c270`:**

```
c270: { type: opencv, index_or_path: '/dev/video4', width: 640, height: 480, fps: 30 }
```

If Step 1 showed the C270 on a different device, use that path in `index_or_path` instead of `/dev/video4`.

### Parameter format

The full `--robot.cameras` argument must be a single string. The value is a map with at least the keys `front` and `c270`. Example:

```
--robot.cameras="{ front: { type: opencv, index_or_path: '/dev/video2', width: 1280, height: 720, fps: 30, fourcc: 'MJPG' }, c270: { type: opencv, index_or_path: '/dev/video4', width: 640, height: 480, fps: 30 } }"
```

Preserve any other keys already present in `--robot.cameras` if the script has them; ensure `front` and `c270` match the values above (with correct device paths from Step 1).

## Edge cases

- **Both cameras not found:** Stop after Step 2. Tell the user which camera is missing and do not modify the script.
- **No suitable `lerobot-*` command:** If the script has no robot command to attach `--robot.cameras` to, say so and ask the user where to add it.
- **Device paths differ:** Always use the device paths identified in Step 1 for USB2.0_CAM1 (for `front`) and for the C270 (for `c270`), not necessarily `/dev/video2` and `/dev/video4`.
