#!/bin/bash

# Upload recorded episodes to Hugging Face Hub
# Activate virtual environment
source /ssd/.venv-lerobot/bin/activate

# For offline testing, set HF_USER manually
HF_USER="skpro19"
echo "HF_USER: $HF_USER"

# Set repository name for upload
REPO_NAME="record-test"
echo "REPO_NAME: $REPO_NAME"

# Set the local directory containing recorded episodes
dir="/home/skpro19/.cache/huggingface/lerobot/$HF_USER/feb20-14_07"
echo "Upload directory: $dir"

# Upload to Hugging Face Hub
huggingface-cli upload $HF_USER/$REPO_NAME "$dir" --repo-type dataset