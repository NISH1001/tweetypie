#!/usr/bin/env python3

import random

from preprocess import (
    preprocess_sentence
)

from data import (
    load_df
)

def create_pairs(text):
    print("Creating bigram pairs...")
    tokens = text.split()
    return list(zip(tokens, tokens[1:]))

def build_trie(pairs):
    print("Building Trie...")
    trie = {}
    for pair in pairs:
        a, b = pair
        if a not in trie:
            trie[a] = {}
        if b not in trie[a]:
            trie[a][b] = 1
        else:
            trie[a][b] += 1
    return trie

def build_probabilities(trie):
    print("Building probabilities...")
    for word, following in trie.items():
        total = sum(following.values())
        for key in following:
            following[key] /= total
    return trie

def generate1(trie, initial_word, max_len=5, verbose=False):
    res = []
    word = initial_word
    while len(res) < max_len:
        if word not in trie:
            break
        transitions = trie[word]
        if verbose:
            print("Current word :: ", word)
            print("Transitions :: ", transitions)
        t = 0
        for w in transitions:
            p = transitions[w]
            t += p
            if t and (random.random() * t) < p:
                next_word = w
            if verbose:
                print(w, p)
        res.append(word)
        word = next_word
    return res

def generate2(trie, initial_word, max_len=5, verbose=False):
    res = []
    word = initial_word
    while len(res) < max_len:
        if word not in trie:
            break
        transitions = trie[word].items()
        transitions_randomized = {w : random.random() * p for w, p in transitions }
        next_state = max(transitions_randomized.items(), key=lambda x : x[1])
        if verbose:
            print("Current word :: ", word)
            print("Transitions :: ", transitions)
            print("Next state :: ", next_state)
        res.append(word)
        word = next_state[0]
    return res

def main():
    tweetfile = "data/tweets/clean/clean.csv"
    df = load_df(tweetfile)
    text = "\n".join(df['text'].values.tolist()).strip()
    pairs = create_pairs(text)
    trie = build_trie(pairs)
    generated_words = generate1(trie, initial_word='i', max_len=15, verbose=False)
    generated_text = ' '.join(generated_words)
    print("Generated tweet::\n{}".format(generated_text))
    print('-'*30)
    print("After preprocessing <SENTENCE>::\n{}".format(preprocess_sentence(generated_text)))


if __name__ == "__main__":
    main()

