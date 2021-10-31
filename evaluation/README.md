Run evaluation on a pretrained model with our chosen Dev tasks:
```
python evaluation/run_eval_harness.py \
	--model gpt2 \
	--model_args pretrained=output/ExamplesStringsCriterion_10k/model \
	--device cuda:0 \
	--tasks headqa,logiqa,mathqa,prost,pubmedqa,qa4mre_2011,qa4mre_2012,qa4mre_2013 \
	--output_path output/eval_results.json
```