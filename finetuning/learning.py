# from transformers import pipeline
# generator = pipeline('text-generation', model='EleutherAI/gpt-neo-125M')
# generator("EleutherAI has", do_sample=True, min_length=50)

import datasets

print(datasets.list_metrics())

for conf in ['boolq', 'cb', 'copa', 'multirc', 'record', 'rte', 'wic', 'wsc', 'wsc.fixed', 'axb', 'axg']:
    super_glue_dataset = datasets.load_dataset('super_glue', conf)
    print(super_glue_dataset)

    metric = datasets.load_metric('super_glue', conf)
    print(metric)