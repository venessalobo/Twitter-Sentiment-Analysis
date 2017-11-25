import sys
import json
import string

from collections import defaultdict


def sent_make_dict(fp):
    sent_dict = {}
    with open(fp) as s:
        for line in s:
            a = str(line).split("\t")
            sent_dict.update({a[0]: int(a[1])})
    return sent_dict


def norm_word(word):
    exclude = set(string.punctuation)
    word = ''.join(ch for ch in word.lower() if ch not in exclude)
    return word


def calc_sent_score(sent_dict, line):
    sent_score = 0
    non_sent_words = []
    for word in line.split(' '):
        if word in sent_dict:
            sent_score += sent_dict[word]
        else:
            non_sent_words.append(word)
    return sent_score, non_sent_words


def update_dict(freq_dict, tweet):
    for word in tweet.split():
        if word in freq_dict:
            freq_dict[word] += 1
        else:
            freq_dict[word] = 1


def main():
    freq_dict = defaultdict()
    tweet_file = open(sys.argv[1])
    # load json file as a dictionary
    for line in tweet_file:
        d = json.loads(line)
        # analyze only english tweets in the text attribute
        if 'text' in d.keys():
            if d['lang'] == 'en':
                # obtain frequency of occurrence of each word in the tweet
                update_dict(freq_dict, norm_word(d['text']))
    # total number of words across all tweets
    tot_occurrence = sum(freq_dict.values())
    for word in freq_dict.keys():
        print(word, freq_dict[word]/float(tot_occurrence))


if __name__ == '__main__':
    main()