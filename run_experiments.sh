#!/bin/bash

# testing-the-waters
# python finetune_with_dataset.py -d configs/dataset/ExamplesStringsCriterion_1k.yaml -f configs/finetune/default.json -m gpt2
# python finetune_with_dataset.py -d configs/dataset/ExamplesStringsCriterion_100k.yaml -f configs/finetune/default.json -m gpt2
# python finetune_with_dataset.py -d configs/dataset/QuestionAnswerStringsV2Criterion_1k.yaml -f configs/finetune/default.json -m gpt2
# python finetune_with_dataset.py -d configs/dataset/QuestionAnswerStringsV2Criterion_100k.yaml -f configs/finetune/default.json -m gpt2
# python finetune_with_dataset.py -d configs/dataset/AllDocuments_1k.yaml -f configs/finetune/default.json -m gpt2
# python finetune_with_dataset.py -d configs/dataset/AllDocuments_100k.yaml -f configs/finetune/default.json -m gpt2

# python finetune_with_dataset.py -d configs/dataset/AllDocuments_1k.yaml -f configs/finetune/default.json -m EleutherAI/gpt-neo-125M
# python finetune_with_dataset.py -d configs/dataset/QuestionAnswerStringsV2Criterion_1k.yaml -f configs/finetune/default.json -m EleutherAI/gpt-neo-125M
# python finetune_with_dataset.py -d configs/dataset/QuestionAnswerStringsV2Criterion_100k.yaml -f configs/finetune/default.json -m EleutherAI/gpt-neo-125M
# python finetune_with_dataset.py -d configs/dataset/ExamplesStringsCriterion_1k.yaml -f configs/finetune/default.json -m EleutherAI/gpt-neo-125M
# python finetune_with_dataset.py -d configs/dataset/ExamplesStringsCriterion_100k.yaml -f configs/finetune/default.json -m EleutherAI/gpt-neo-125M
# python finetune_with_dataset.py -d configs/dataset/AllDocuments_100k.yaml -f configs/finetune/default.json -m EleutherAI/gpt-neo-125M


# pretrained-baselines
# python finetune_with_dataset.py -d configs/dataset/AllDocuments_1k.yaml -f configs/finetune/default.json -m gpt2-xl
# python finetune_with_dataset.py -d configs/dataset/AllDocuments_1k.yaml -f configs/finetune/default.json -m gpt2-large
# python finetune_with_dataset.py -d configs/dataset/AllDocuments_1k.yaml -f configs/finetune/default.json -m gpt2-medium
# python finetune_with_dataset.py -d configs/dataset/AllDocuments_1k.yaml -f configs/finetune/default.json -m gpt2
# python finetune_with_dataset.py -d configs/dataset/QuestionAnswerStringsV2Criterion_1k.yaml -f configs/finetune/default.json -m EleutherAI/gpt-neo-125M
# python finetune_with_dataset.py -d configs/dataset/QuestionAnswerStringsV2Criterion_1k.yaml -f configs/finetune/default.json -m EleutherAI/gpt-neo-1.3B
# python finetune_with_dataset.py -d configs/dataset/QuestionAnswerStringsV2Criterion_1k.yaml -f configs/finetune/default.json -m EleutherAI/gpt-neo-2.7B
# python finetune_with_dataset.py -d configs/dataset/QuestionAnswerStringsV2Criterion_1k.yaml -f configs/finetune/default.json -m EleutherAI/gpt-j-6B


# first-batch-train
# python finetune_with_dataset.py -d configs/dataset/AllDocuments_1k.yaml -f configs/finetune/default.json -m gpt2-large
# python finetune_with_dataset.py -d configs/dataset/QuestionAnswerStringsV2Criterion_1k.yaml -f configs/finetune/default.json -m gpt2-large
# python finetune_with_dataset.py -d configs/dataset/QuestionAnswerStringsV2Criterion_100k.yaml -f configs/finetune/default.json -m gpt2-large
# python finetune_with_dataset.py -d configs/dataset/ExamplesStringsCriterion_100k.yaml -f configs/finetune/default.json -m gpt2-large

# python finetune_with_dataset.py -d configs/dataset/AllDocuments_1k.yaml -f configs/finetune/default.json -m EleutherAI/gpt-neo-1.3B
# python finetune_with_dataset.py -d configs/dataset/QuestionAnswerStringsV2Criterion_1k.yaml -f configs/finetune/default.json -m EleutherAI/gpt-neo-1.3B
# python finetune_with_dataset.py -d configs/dataset/QuestionAnswerStringsV2Criterion_100k.yaml -f configs/finetune/default.json -m EleutherAI/gpt-neo-1.3B
# python finetune_with_dataset.py -d configs/dataset/ExamplesStringsCriterion_100k.yaml -f configs/finetune/default.json -m EleutherAI/gpt-neo-1.3B

# python finetune_with_dataset.py -d configs/dataset/AllDocuments_1k.yaml -f configs/finetune/default.json -m gpt2-medium
# python finetune_with_dataset.py -d configs/dataset/QuestionAnswerStringsV2Criterion_1k.yaml -f configs/finetune/default.json -m gpt2-medium
# python finetune_with_dataset.py -d configs/dataset/QuestionAnswerStringsV2Criterion_100k.yaml -f configs/finetune/default.json -m gpt2-medium
# python finetune_with_dataset.py -d configs/dataset/ExamplesStringsCriterion_100k.yaml -f configs/finetune/default.json -m gpt2-medium


# Build slow datasets
# time python finetune_with_dataset.py -d configs/dataset/ExamplesStringsCriterion_t1k.yaml
# time python finetune_with_dataset.py -d configs/dataset/ExamplesStringsCriterion_t5k.yaml
# time python finetune_with_dataset.py -d configs/dataset/ExamplesStringsCriterion_t20k.yaml
# time python finetune_with_dataset.py -d configs/dataset/ExamplesStringsCriterion_t200k.yaml
# time python finetune_with_dataset.py -d configs/dataset/QuestionAnswerStringsV2Criterion_t1M.yaml
# time python finetune_with_dataset.py -d configs/dataset/QuestionAnswerStringsV2Criterion_t10M.yaml