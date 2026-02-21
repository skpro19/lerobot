# LeRobot Train Parameters

This document lists all parameters that can be passed to the `lerobot-train` command, organized into logical buckets.

## Core Training Parameters

- `output_dir`: Output directory for saving training artifacts (Path)
- `job_name`: Name for the training job (str)
- `resume`: Resume training from checkpoint (bool, default: False)
- `seed`: Random seed for training and evaluation (int, default: 1000)
- `num_workers`: Number of dataloader workers (int, default: 4)
- `batch_size`: Training batch size (int, default: 8)
- `steps`: Total training steps (int, default: 100_000)
- `save_checkpoint`: Whether to save checkpoints (bool, default: True)
- `save_freq`: Checkpoint save frequency in steps (int, default: 20_000)
- `use_policy_training_preset`: Use policy's built-in training presets (bool, default: True)

## Dataset Parameters

- `dataset.repo_id`: Hugging Face dataset repository ID (str)
- `dataset.root`: Local dataset root directory (str)
- `dataset.episodes`: List of episode indices to use (list[int])
- `dataset.revision`: Dataset revision/tag (str)
- `dataset.use_imagenet_stats`: Use ImageNet normalization stats (bool, default: True)
- `dataset.video_backend`: Video decoding backend (str, default: auto-detected)
- `dataset.streaming`: Use streaming mode for large datasets (bool, default: False)

## Image Transform Parameters

- `dataset.image_transforms.enable`: Enable image augmentations (bool, default: False)
- `dataset.image_transforms.max_num_transforms`: Max transforms per image (int, default: 3)
- `dataset.image_transforms.random_order`: Apply transforms in random order (bool, default: False)
- `dataset.image_transforms.tfs.<name>`: Per-transform config (e.g. brightness, contrast, saturation, hue, sharpness, affine). Each has:
  - `weight`: Sampling weight (float, default: 1.0)
  - `type`: Transform class name, e.g. "ColorJitter", "RandomAffine" (str)
  - `kwargs`: Dict of bounds/args for the transform (e.g. `{"brightness": (0.8, 1.2)}`)

## Policy/Model Parameters

- `policy.type`: Policy type (str, e.g., "act", "diffusion", etc.)
- `policy.path`: Path or HuggingFace repo ID of pretrained policy (str); when set, config is loaded from here and CLI overrides apply
- `policy.n_obs_steps`: Number of observation steps (int, default: 1)
- `policy.input_features`: Input feature specifications (dict)
- `policy.output_features`: Output feature specifications (dict)
- `policy.device`: Device for policy (str, e.g., "cuda", "cpu")
- `policy.use_amp`: Use automatic mixed precision (bool, default: False)
- `policy.use_peft`: Use parameter-efficient fine-tuning (bool, default: False)
- `policy.push_to_hub`: Push model to Hugging Face Hub (bool, default: True)
- `policy.repo_id`: Repository ID for model upload (str)
- `policy.private`: Make repository private (bool)
- `policy.tags`: Tags for the model (list[str])
- `policy.license`: License for the model (str)
- `policy.pretrained_path`: Path to pretrained model (Path; set automatically when using `policy.path`)
- `policy.drop_n_last_frames`: Frames to drop from end of each episode for sampling (int; used by e.g. diffusion, sarm)

## Optimizer Parameters

- `optimizer.type`: Optimizer type ("adam", "adamw", "sgd", "xvla-adamw", "multi_adam")
- `optimizer.lr`: Learning rate (float)
- `optimizer.weight_decay`: Weight decay (float)
- `optimizer.grad_clip_norm`: Gradient clipping norm (float)

### Adam-specific
- `optimizer.betas`: Adam beta parameters (tuple[float, float])
- `optimizer.eps`: Adam epsilon (float)

### AdamW-specific
- `optimizer.betas`: AdamW beta parameters (tuple[float, float])
- `optimizer.eps`: AdamW epsilon (float)

### SGD-specific
- `optimizer.momentum`: SGD momentum (float)
- `optimizer.dampening`: SGD dampening (float)
- `optimizer.nesterov`: Use Nesterov momentum (bool)

### XVLA-AdamW-specific
- `optimizer.soft_prompt_lr_scale`: Soft prompt learning rate scale (float, default: 1.0)
- `optimizer.soft_prompt_warmup_lr_scale`: Warmup scale for soft prompts (float)

### Multi-Adam-specific
- `optimizer.optimizer_groups`: Dictionary of optimizer group configurations (dict)

## Learning Rate Scheduler Parameters

- `scheduler.type`: Scheduler type ("diffuser", "vqbet", "cosine_decay_with_warmup")

### Diffuser scheduler
- `scheduler.name`: Scheduler name (str, default: "cosine")
- `scheduler.num_warmup_steps`: Warmup steps (int)

### VQBeT scheduler
- `scheduler.num_warmup_steps`: Warmup steps (int)
- `scheduler.num_vqvae_training_steps`: VQ-VAE training steps (int)
- `scheduler.num_cycles`: Number of cosine cycles (float, default: 0.5)

### Cosine decay with warmup
- `scheduler.num_warmup_steps`: Warmup steps (int)
- `scheduler.num_decay_steps`: Decay steps (int)
- `scheduler.peak_lr`: Peak learning rate (float)
- `scheduler.decay_lr`: Final decay learning rate (float)

## Evaluation Parameters

- `eval_freq`: Evaluation frequency in steps (int, default: 20_000)
- `eval.n_episodes`: Number of evaluation episodes (int, default: 50)
- `eval.batch_size`: Evaluation batch size (int, default: 50)
- `eval.use_async_envs`: Use asynchronous environments (bool, default: False)

## Environment Parameters

- `env.type`: Environment type (str, e.g., "aloha", "pusht", "libero", "metaworld", "gym_manipulator", "isaaclab_arena")
- `env.task`: Specific task within environment (str)
- `env.episode_length`: Maximum steps per episode (int, environment-specific defaults)
- `env.fps`: Environment FPS (int, default: 30)
- `env.max_parallel_tasks`: Maximum parallel tasks (int, default: 1)
- `env.disable_env_checker`: Disable gym environment checker (bool, default: True)
- `env.features`: Policy feature definitions for env (dict; advanced)
- `env.features_map`: Mapping from env keys to policy keys (dict; advanced)

### Environment-specific parameters (vary by type)

#### Aloha
- `episode_length`, `obs_type`, `observation_height`, `observation_width`, `render_mode`

#### Pusht
- `episode_length`, `obs_type`, `render_mode`, `visualization_width`, `visualization_height`

#### Libero
- `episode_length`, `obs_type`, `render_mode`, `camera_name`, `camera_name_mapping`, `init_states`, `observation_height`, `observation_width`, `control_mode`

#### Metaworld
- `episode_length`, `obs_type`, `render_mode`, `multitask_eval`

#### Gym Manipulator
- `robot`, `teleop`, `processor` (complex nested config)

#### IsaacLab Arena
- `hub_path`, `episode_length`, `num_envs`, `embodiment`, `object`, `mimic`, `teleop_device`, `seed`, `device`, `disable_fabric`, `enable_cameras`, `headless`, `enable_pinocchio`, `environment`, `state_dim`, `action_dim`, `camera_height`, `camera_width`, `video`, `video_length`, `video_interval`, `state_keys`, `camera_keys`, `kwargs` (extra fields passed to hub make_env)

## Weights & Biases Parameters

- `wandb.enable`: Enable W&B logging (bool, default: False)
- `wandb.disable_artifact`: Disable artifact upload (bool, default: False)
- `wandb.project`: W&B project name (str, default: "lerobot")
- `wandb.entity`: W&B entity/team (str)
- `wandb.notes`: Run notes (str)
- `wandb.run_id`: Specific run ID (str)
- `wandb.mode`: W&B mode ("online", "offline", "disabled")

## PEFT Parameters

- `peft.target_modules`: Target modules for PEFT (list[str] | str)
- `peft.full_training_modules`: Modules to train fully (list[str])
- `peft.method_type`: PEFT method ("LORA", etc.) (str, default: "LORA")
- `peft.init_type`: Initialization type (str)
- `peft.r`: PEFT rank (int, default: 16)

## RA-BC (Reward-Aligned Behavior Cloning) Parameters

- `use_rabc`: Enable reward-weighted training (bool, default: False)
- `rabc_progress_path`: Path to precomputed SARM progress (str)
- `rabc_kappa`: Hard threshold for high-quality samples (float, default: 0.01)
- `rabc_epsilon`: Numerical stability constant (float, default: 1e-6)
- `rabc_head_mode`: Dual-head model mode ("sparse" or "dense")

## Miscellaneous Parameters

- `log_freq`: Logging frequency in steps (int, default: 200)
- `tolerance_s`: Tolerance in seconds (float, default: 1e-4)
- `rename_map`: Observation key renaming map (dict[str, str])
- `config_path`: Path to `train_config.json` (or directory containing it); required when `resume=true` to load run config and checkpoint (str)

## Advanced/Plugin Parameters

- `env.discover_packages_path`: Plugin discovery path for environments
- Various plugin and third-party extension parameters

## Usage Notes

Parameters are passed using dot notation (e.g., `--policy.type=act`, `--dataset.repo_id=username/dataset`). The actual available parameters may vary depending on the specific policy type and environment being used. Some parameters are conditionally available based on the chosen components. Default values are indicated where available in the codebase.

When using `--policy.path=<repo_or_dir>`, the full policy config is loaded from that path; any `--policy.<key>=<value>` passed on the CLI overrides those values. So policy-type-specific params (e.g. ACT's `n_encoder_layers`, diffusion's `n_action_steps`) are not listed above but can be overridden the same way once the policy type is known.

Example usage:
```bash
lerobot-train \
    --policy.type=act \
    --policy.path=<hf_username>/<policy_name> \
    --dataset.repo_id=<hf_username>/<dataset_name> \
    --output_dir=outputs/train/my_experiment \
    --job_name=my_act_training \
    --batch_size=8 \
    --steps=100000 \
    --wandb.enable=true \
    --wandb.project=my_project \
    --eval_freq=20000 \
    --save_freq=20000
```