#!/usr/bin/env python3

from collections import defaultdict
import random

from preprocess import (
    preprocess_sentence
)

from data import (
    load_df
)

class MarkovChain:
    def __init__(self, lookback=2):
        self.trie = defaultdict(lambda : defaultdict(int))
        self.lookback = lookback
        self.tweets = []

    def train(self, lines):
        """
            Build markov model
        """
        self.tweets += lines
        print("Building trie...")
        for title in lines:
            tokens = title.split()
            if len(tokens) > self.lookback:
                for i in range(len(tokens) + 1):
                    a = ' '.join(tokens[max(0, i-self.lookback) : i])
                    b = ' '.join(tokens[i : i+1])
                    self.trie[a][b] += 1
        self._build_probabilities()

    def _build_probabilities(self):
        """
            Calculate probabilities
        """
        print("Building probabilities...")
        for word, following in self.trie.items():
            total = float(sum(following.values()))
            for key in following:
                following[key] /= total

    def _sample(self, items):
        next_word = None
        t = 0.0
        for k, v in items:
            t += v
            if t and random.random() < v/t:
                next_word = k
        return next_word

    def generate(self, initial_words=[]):
        sentence = initial_words[:-1]
        next_word = self._sample(self.trie[''].items()) if not initial_words else initial_words[-1]
        while next_word != '':
            sentence.append(next_word)
            next_word = self._sample(self.trie[' '.join(sentence[-self.lookback:])].items())
        sentence = ' '.join(sentence)
        return sentence
        # flag = True

        # # Prune lines that are substrings of actual lines
        # for tweet in self.tweets:
        #     if sentence in tweet:
        #         flag = False
        #         break
        # if flag:
        #     sentences.append(sentence)
        # return sentences


def main():
    tweetfile = "data/tweets/clean/clean.csv"
    # df = load_df(tweetfile)
    mc = MarkovChain(lookback=2)
    mc.train(load_df(tweetfile)['text'].values.tolist())

    # initial_words = ['we', 'tend', 'to']
    initial_words = ['life', 'is']
    tweet = mc.generate(initial_words)
    print("Generated tweet::\n{}".format(tweet))
    print('-'*30)
    print("After preprocessing <SENTENCE>::\n{}".format(preprocess_sentence(tweet)))

if __name__ == "__main__":
    main()

