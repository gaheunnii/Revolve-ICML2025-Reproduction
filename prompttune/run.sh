#!/bin/bash

# Example run script for PromptTune

# Run v1_momentum optimizer
python -m evaluation.instancep_opt \
  --task GSM8K_DSPy \
  --backbone_engine ollama-gpt-oss:120b \
  --model ollama-gpt-oss:120b \
  --optimizer_version v1_momentum \
  --num_threads 1