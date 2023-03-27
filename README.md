# Neural Machine Translation in PyTorch
**Ken Sible | [NLP Group](https://nlp.nd.edu)** | **University of Notre Dame**

Note, any option in `model.config` can also be passed as a command line argument.
```
$ python translate.py --lang de en --beam_size 10 --string "Ich liebe Übersetzungen!"
```

Additionally, any command line output can be redirected from `stdout` to a file.
```
$ python translate.py --lang de en --file infile.txt > outfile.txt
```

## Train Model
```
usage: main.py [-h] --lang LANG LANG [--data FILE] [--test FILE] [--vocab FILE] [--config FILE] [--load FILE] [--save FILE] [--seed SEED] [--tqdm]

optional arguments:
  -h, --help        show this help message and exit
  --lang LANG LANG  source/target language
  --data FILE       training data
  --test FILE       validation data
  --vocab FILE      shared vocab
  --config FILE     model config
  --load FILE       load state_dict
  --save FILE       save state_dict
  --seed SEED       random seed
  --tqdm            toggle tqdm
```

## Score Model
```
usage: score.py [-h] --lang LANG LANG [--data FILE] [--vocab FILE] [--config FILE] [--load FILE]

optional arguments:
  -h, --help        show this help message and exit
  --lang LANG LANG  source/target language
  --data FILE       testing data
  --vocab FILE      shared vocab
  --config FILE     model config
  --load FILE       load state_dict
```

## Translate Input
```
usage: translate.py [-h] --lang LANG LANG [--vocab FILE] [--codes FILE] [--config FILE] [--load FILE] (--file FILE | --string STRING | --interactive)

optional arguments:
  -h, --help        show this help message and exit
  --lang LANG LANG  source/target language
  --vocab FILE      shared vocab
  --codes FILE      shared codes
  --config FILE     model config
  --load FILE       load state_dict
  --file FILE       input file
  --string STRING   input string
  --interactive     interactive session
```

## Model Configuration (Default)
```
embed_dim           = 512   # dimensions of embedding sublayers
ff_dim              = 2048  # dimensions of feed-forward sublayers
num_heads           = 8     # number of parallel attention heads
num_layers          = 6     # number of encoder/decoder layers
dropout             = 0.3   # dropout for feed-forward/attention sublayers
max-epochs          = 50    # maximum number of epochs, halt training
lr                  = 3e-4  # learning rate (step size of optimizer)
patience            = 3     # number of epochs without improvement
decay-factor        = 0.8   # if patience reached, lr *= decay-factor
min-lr              = 5e-5  # minimum learning rate, halt training
label-smoothing     = 0.1   # label smoothing (regularization technique)
batch-size          = -1    # number of tokens (source + target) per batch;
                            # if batch-size = -1, fill available GPU memory
                            # using max-length and binary search
max-length          = 256   # maximum sentence length (if batch-size = -1)
beam-width          = 4     # beam search and length normalization
```
