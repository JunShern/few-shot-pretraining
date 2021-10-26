# (WIP)

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