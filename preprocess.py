#!/usr/bin/env python3

import re
import itertools
import nltk

def preprocess_sentence(text):
    sentences = re.split(r'\s*<SENTENCE>\s*', text)
    return '.\n'.join([sentence.capitalize() for sentence in sentences ]).strip()

def remove_emoticons(text, emoticons):
    for emoticon in emoticons:
        if emoticon in text:
            # text = re.sub(r"\s+{}\s*".format(emoticon), '<EMOTICON>', text)
            text = text.replace(emoticon, '<EMOTICON>')
    return text

def add_sentence_boundary(text):
    text = re.sub(r'[!?;.]{2,}', '. ', text)
    tokenizer = nltk.tokenize.PunktSentenceTokenizer()
    sentences = tokenizer.tokenize(text)
    return ' <SENTENCE> '.join(sentences)

def clean_text(text):
    text = text.encode('ascii', errors='ignore').decode()
    text = text.lower()
    text = re.sub(r'http\S+', ' ', text)
    # text = re.sub(r'#+', ' ', text )
    text = re.sub(r'#[A-Za-z0-9]+', ' ', text)
    text = re.sub(r'@[A-Za-z0-9_]+', ' ', text)
    text = re.sub(r"([A-Za-z]+)'s", r"\1 is", text)
    text = re.sub(r"\'ve", " have ", text)
    text = re.sub(r"won't", "will not ", text)
    text = re.sub(r"isn't", "is not ", text)
    text = re.sub(r"can't", "can not ", text)
    text = re.sub(r"n't", " not ", text)
    text = re.sub(r"i'm", "i am ", text)
    text = re.sub(r"\'re", " are ", text)
    text = re.sub(r"\'d", " would ", text)
    text = re.sub(r"\'ll", " will ", text)
    text = re.sub('["\[\]_()?;:,./+-]+', ' ', text)
    text = re.sub(r'\d+', ' ', text)
    text = re.sub('\s+', ' ', text)
    text = text.replace("<sentence>", "<SENTENCE>")
    text = text.strip()
    return text

def remove_stopwords(text, stopwords):
    tokens = text.split()
    res = []
    for token in tokens:
        if token not in stopwords:
            res.append(token)
    return ' '.join(res)

def clean_all(text, emoticons, stopwords, remove_stop=True):
    text = add_sentence_boundary(text)
    text = clean_text(text)
    text = remove_emoticons(text, emoticons)
    if remove_stop:
        text = remove_stopwords(text, stopwords)
    return  text




def main():
    text = "Hello! I am paradox. I am a bot."
    print(add_sentence_boundary(text))

if __name__ == "__main__":
    main()

