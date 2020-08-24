import MeCab
import numpy as np

import re
from collections import Counter
from random import random

from twitter import Twitter

class Trigram:

    def __init__(self, corpus: list):
        self.raw_corpus_ = corpus
        self.trigram_ = []
        self.dic3 = None
        self.usage_ = []
        self._tinified_corpus()
        self._create_trigram()
        self._create_usage()

    def _tinified_corpus(self):
        corpus = [re.sub('(\n)+|\\s|(#|http(s*)://)[a-zA-Z0-9./]*|(ー|-)+|,+|(\.)+|、+|。+|(|)|（|）|(!|\?)+', '', item) for item in self.raw_corpus_]
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
        wakati = MeCab.Tagger('-Owakati -d /usr/local/lib/mecab/dic/mecab-ipadic-neologd')
        for target in self.corpus_:
            target = wakati.parse(target).split(' ')
            for words in zip(target[0:], target[1:], target[2:]):
                self.trigram_.append(tuple(words))

        self.dic3 = Counter(self.trigram_)

        return self

    def _generate_unit(self, word):
        dic = self.dic3
        matched = []

        if type(word) == str:
            matched = np.array(list(
                filter((lambda x: x[0][0] == word) or (lambda x: x[0][1] == word),
                        dic.items())
            ))
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
                ))
                if len(matched) == 0:
                    return False
                probas = [count[1] for count in matched]
                weights = np.random.rand(len(matched)) * probas
                self.current_units_ = [word[1], matched[np.argmax(weights)][0][2]]

        return True

    def _create_usage(self):
        for words in self.trigram_:
            listed = list(words)
            if listed:
                self.usage_.extend(listed)
        self.usage_ = set(self.usage_)

        return self


    def generate(self, word):
        output = word
        word = word
        while True:
            if not self._generate_unit(word):
                break
            word = self.current_units_
            output += word[1]

        return output

if __name__ == "__main__":
    tri = Trigram(['\nあ\nアイウエオ\n', 'ー', 'ーーーーーーーー'])
    
    
    