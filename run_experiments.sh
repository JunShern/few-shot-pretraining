#!/bin/bash

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

# pretrained_baselines
# python finetune_with_dataset.py -d configs/dataset/AllDocuments_1k.yaml -f configs/finetune/default.json -m gpt2-xl
# python finetune_with_dataset.py -d configs/dataset/AllDocuments_1k.yaml -f configs/finetune/default.json -m gpt2-large
# python finetune_with_dataset.py -d configs/dataset/AllDocuments_1k.yaml -f configs/finetune/default.json -m gpt2-medium
# python finetune_with_dataset.py -d configs/dataset/AllDocuments_1k.yaml -f configs/finetune/default.json -m gpt2