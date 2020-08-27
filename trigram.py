import MeCab
import numpy as np

import re
from collections import Counter
from random import random

from twitter import Twitter

class Trigram:
    """This is Trigram class"""

    def __init__(self, corpus: list):
        """
        Initialize variable
        """
        self.raw_corpus_ = corpus
        self.trigram_ = []
        self.dic3 = None
        self.usage_ = []
        self._tinified_corpus()
        self._create_trigram()
        self._create_usage()

    def _tinified_corpus(self):
        """"
        Tinifiy a given corpus,
        and then generate numpy array of tweets text.

        Finally, it return itself.
        """
        corpus = [re.sub(r'\n+|\s|(#|http(s*)://)[a-zA-Z0-9./]*|-+|,+|\.+|、+|。+|(\(|\))+|（|）|(!|\?)+|(！|？)+|(;|:)+|\^|\$|\^|(\'|")+|%+|{+|}+|/+|=+', '', item) for item in self.raw_corpus_]
        with open('ignore_words.txt', mode='r', encoding='utf-8') as f:
            print('以下がコーパス除外単語です')
            ignore = re.sub(r'\n', '', f.readline())
            print(ignore)
            corpus = [re.sub(ignore, '', item) for item in corpus]
            while ignore:
                ignore = re.sub('\n', '', f.readline())
                if ignore is not '' or ignore is not '\n':
                    print(ignore)
                    corpus = [re.sub(ignore, '', item) for item in corpus]

        self.corpus_ = np.array(corpus)
        
        return self

    def _create_trigram(self):
        """"
        Create trigram.
        This is list including tuple which has three words.

        Finally, it return itself.
        """
        wakati = MeCab.Tagger('-Owakati -d /usr/local/lib/mecab/dic/mecab-ipadic-neologd')
        for target in self.corpus_:
            target = wakati.parse(target).split(' ')
            for words in zip(target[0:], target[1:], target[2:]):
                self.trigram_.append(tuple(words))

        self.dic3 = Counter(self.trigram_)

        return self

    def _generate_unit(self, word):
        """
        This is used in the generate function.

        This return boolean, True or False.
        """
        dic = self.dic3
        matched = []

        if type(word) == str:
            matched = np.array(list(
                filter((lambda x: x[0][0] == word) or (lambda x: x[0][1] == word),
                        dic.items())
            ), dtype='object')
            if len(matched) == 0:
                print('マッチするパターンがなかったため入力値がそのまま出力されます')
                return False

            probas = [count[1] for count in matched]
            weights = np.random.rand(len(matched)) * probas
            for i, w in enumerate(matched[np.argmax(weights)][0]):
                if w == word:
                    self.current_units_ = [word, matched[np.argmax(weights)][0][i+1]]

        elif type(word) == list:
            if len(word) >= 2:
                matched = np.array(list(
                filter((lambda x: x[0][0] == word[0]) or (lambda x: x[0][1] == word[2]),
                        dic.items())
                ), dtype='object')
                if len(matched) == 0:
                    return False
                probas = [count[1] for count in matched]
                weights = np.random.rand(len(matched)) * probas
                if np.max(weights) > proba_rate * len(self.output):
                    self.current_units_ = [word[1], matched[np.argmax(weights)][0][2]]
                else:
                    return False

        return True

    def _create_usage(self):
        """
        This can show words list you can select for starting word of sentence
        """
        for words in self.trigram_:
            listed = list(words)
            if listed:
                self.usage_.extend(listed)
        self.usage_ = set(self.usage_)

        return self


    def generate(self, word, proba_rate=0.08):
        """
        This can generate sentence using Trigram
        """
        self.output = word
        word = word
        while True:
            if not self._generate_unit(word, proba_rate):
                break
            word = self.current_units_
            self.output += word[1]

        return self.output
