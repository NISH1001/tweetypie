# tweetypie
A naive tweet generator and analysis of personal Twitter data

## Preprocess
Use `data.py` directly to process and clean everything. This includes:
- removal of links
- removal of hashtags
- removal of @username mentions
- addition of sentence boundaries (done using simple ntlk tokenization)
- expansion of common acronyms like **we'll**, **i've**,...
- removal of textual emoticons like **:D**, **:P**, ...

Run directly as:
```bash
python data.py
```

Be sure to change `src` and `dest` variable accordingly.

## Data 
Data is provided by Twitter itself. Just go to the settings and download your profile archives. It will give a zip file.  
Extract and find the directory `data/js/tweets/`. There wll be the data in JS format. So, preprocessing is done accordingly.

## Data Directory In This repo
```bash
data/
    |- tweets/
        |- original/
        |- samples/
        |- clean/
    |- emoticons.txt
```
I have provided few samples inside `samples/` directory for a reference.

Once preprocessing is done, there will be `clean.csv` file generated inside `clean/` directory. 

## Special Tokens
There are two tokens:
- **&lt;EMOTICON&gt;** : A general token for all textual emoticons/smileys
- **&lt;SENTENCE&gt;** : Start/End of sentence

## Tweet Generation
Tweets are generated using simple markov chain. The details can also be found in [this](tweet-generator-markov.ipynb) notebook.  

`tweetgen.py` is used for simple chain that only sees one past word and predicts one new word.  
`tweetgen2.py` is used for introducing the concept of **lookback** that can see **n** past words and generate a new word accordingly.

## Markov Sample Tweets
Some tweets generated using `tweetgen2.py` are:
```bash
- i do not really need such specs for a $ <SENTENCE> i have it in just one shot do not even bat an eye on this matter <SENTENCE>
- haha <SENTENCE> yo week sablai tattoo hanna mann lagyra raicha <SENTENCE> <EMOTICON>
- folks here falling in love with the consequences of availability of data re <SENTENCE> ekdumai thulo <SENTENCE> huge and enormous amount of data re <SENTENCE> kandai vayecha <EMOTICON>
```

Some tweetgs generated using `tweetgen.py` are:
```bash
- i have never know yourself some deeds <SENTENCE> kill him <SENTENCE> dyang <SENTENCE> simulation and
- i succeed i am pretty refreshing <SENTENCE> haha <SENTENCE> = ! <SENTENCE> the mind like
- i had composed years <SENTENCE> <EMOTICON> how earth a smoother time perception while solitude said
```


## Note
This repo is meant as an analysis of my previous Twitter account which I have deleted due to some circumstances.  
The focus is not only on generation, but also on analysis.
