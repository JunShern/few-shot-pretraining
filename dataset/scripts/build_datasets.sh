#!/bin/bash

python dataset/build_dataset.py -c configs/dataset/AllDocuments_1k.yaml
python dataset/build_dataset.py -c configs/dataset/AllDocuments_100k.yaml

python dataset/build_dataset.py -c configs/dataset/ExamplesStringsCriterion_1k.yaml
python dataset/build_dataset.py -c configs/dataset/ExamplesStringsCriterion_100k.yaml

python dataset/build_dataset.py -c configs/dataset/QuestionAnswerStringsV2Criterion_1k.yaml
python dataset/build_dataset.py -c configs/dataset/QuestionAnswerStringsV2Criterion_100k.yaml