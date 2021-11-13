#!/usr/bin/env python

from datasets import load_dataset

# dataset = load_dataset('c4', 'en', cache_dir="./base_datasets/c4")
dataset = load_dataset('c4', 'en', split='validation', cache_dir="./base_datasets/c4")
