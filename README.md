# Tweet imitator

You can generate some words or a sentence.

## Features

This generates sentence using Trigram based on your Twitter texts (within 7 days).

When there is a past corpus in the directory *tweet-imitator* and this refer to the corpus in main.py, you can use it or add new corpus to it.

## Environments

- mecab-python3==1.0.1
- oauthlib==3.1.0
- requests==2.24.0
- requests-oauthlib==1.3.0
- numpy==1.18.5

*You need **Mecab** on your computer.*

You should visit Mecab official Web site [here](https://taku910.github.io/mecab) if Mecab or Mecab additional dictionary is not on your PC.

## Create Environments

```terminal or prompt
pip install -r requirements.txt
```

## Run this script

```terminal or prompt
python main.py
```

## Customize this script

### Not use neo-dictionary

When you would not like to use *neo-dictionary(additional dictionary)*, you will rewrite *main.py*.

```Python @ main.py before rewriting
......
def _create_trigram(self):
        wakati = MeCab.Tagger('-Owakati -d /usr/local/lib/mecab/dic/mecab-ipadic-neologd') <--- here
        for target in self.corpus_:
            target = wakati.parse(target).split(' ')
......
```

You should change the script to the following script.  

```Python @ main.py after rewriting
......
def _create_trigram(self):
        wakati = MeCab.Tagger('-Owakati) <--- here
        for target in self.corpus_:
            target = wakati.parse(target).split(' ')
......
```