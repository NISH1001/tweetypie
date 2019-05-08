#!/usr/bin/env python3

"""
    This module is intended to clean my personal tweet data from Twitter
    and then dump them into a csv
"""

import glob
import json
import pathlib
import os
import pandas as pd

from preprocess import (
    add_sentence_boundary,
    clean_text,
    remove_emoticons
)

def load_emoticons(filename):
    with open(filename) as f:
        return f.read().split()

def clean(emoticons, src="data/tweets/original", dest="data/tweets/clean/"):
    """
        Clean Tweet:
            - remove @username mentions
            - remove http
            - expand basic acronyms like we'll -> we will
            - remove emoticons
    """
    print("Cleaing tweets...")
    src = os.path.join(src, '*')
    files = sorted(glob.glob(src))
    for filename in files:
        print("Loading from {}".format(filename))
        fn = os.path.splitext(os.path.basename(filename))[0]
        with open(filename) as f:
            f.readline()
            data = []
            for d in json.load(f):
                text = d['text']
                text = add_sentence_boundary(text)
                text = clean_text(text)
                text = remove_emoticons(text, emoticons)
                data.append({'text': text, 'created_at': d['created_at']})
        dumpname = os.path.join(dest, fn) + '.json'
        print("Dumping to {}".format(dumpname))
        with open(dumpname, 'w') as f:
            json.dump(data, f)

def dump_as_csv(src="data/tweets/clean", dest="data/tweets/clean.csv"):
    print("Dumping to {}".format(dest))
    data = []
    src = os.path.join(src, '*')
    files = sorted(glob.glob(src))
    for filename in files:
        with open(filename) as f:
            d = json.load(f)
            data += d
    df = pd.DataFrame(data)
    df.to_csv(dest, index=False)

def load_df(filename):
    print("Loading pandas dataframe from {}".format(filename))
    df = pd.read_csv(filename)
    df['created_at'] = pd.to_datetime(df['created_at'])
    df = df.dropna()
    df = df.sort_values(by='created_at')
    return df

def main():
    text = "Hello :D I am paradox :)"
    src = "data/tweets/original"
    dest = "data/tweets/clean"
    emoticons = load_emoticons("data/emoticons.txt")
    clean(emoticons, src, dest)
    dump_as_csv(dest, "data/tweets/clean.csv")

if __name__ == "__main__":
    main()

