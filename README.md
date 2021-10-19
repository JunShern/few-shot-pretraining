# Few-shot Pretraining

## Install
```bash
conda create -n alignment python=3.8
conda activate alignment
pip install -r requirements.txt
```

## Build dataset example
Build a small test dataset:
```
python build_dataset.py -c configs/dataset/ExamplesStringsCriterion_10k.yaml
```

Visualize outputs:
```
cd streamlit
streamlit run browse_results.py -- --data-dir ../test-output
```

## Evaluate model example
Clone the [lm-evaluation-harness](https://github.com/EleutherAI/lm-evaluation-harness) repo adjacent to this one:
```
junshern@work ⚒  tree git/ -L 1
git/
├── few-shot-pretraining
└── lm-evaluation-harness
```
Install deps
```
cd lm-evaluation-harness
pip install lm-eval
```
Run evaluation with our chosen Dev tasks
```
python main.py \
	--model gpt2 \
	--device cuda:0 \
	--tasks headqa,logiqa,mathqa,prost,pubmedqa,qa4mre_2011,qa4mre_2012,qa4mre_2013
```

## Idealized workflow (WIP)
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