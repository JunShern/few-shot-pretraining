# Few-shot Pretraining

Idealized workflow:
```bash
# Build finetune dataset with `ExamplesStringsCriterion` (small one first, e.g. 10k docs?)
build_dataset.py
--base-datasets Pile C4
--criterion ExamplesStringsCriterion
--num-docs 10000
--out-dir path/to/dataset
# build_dataset.py
# --config configs/dataset/ExamplesStringsCriterion_10k.yaml

# Setup code to evaluate a model on some task set (dev or test)
evaluate_model.py
--model GPT-Neo # or path/to/model
--task 

# Setup code to finetune model with GPU on finetune datasets
finetune.py
--base-model GPT-Neo
--dataset path/to/dataset
```

Currently working example:
```
python build_dataset.py -c configs/dataset/ExamplesStringsCriterion_10k.yaml
streamlit run browse_results.py -- --data-dir ../test-output
```