#!/bin/bash

# For offline testing, set HF_USER manually
HF_USER="skpro19"
echo "HF_USER: $HF_USER"

lerobot-train \
  --batch_size=2 \
  --num_workers=1 \
  --dataset.repo_id=${HF_USER}/zandu-balm-Feb20-14-07 \
  --policy.type=act \
  --output_dir=outputs/train/act_zandu-balm-Feb20-14-07 \
  --job_name=act_zandu-balm-Feb20-14-07 \
  --policy.device=cuda \
  --wandb.enable=true \
  --policy.repo_id=${HF_USER}/act_zandu-balm-Feb20-14-07