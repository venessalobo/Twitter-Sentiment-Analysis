import sys
import json


def hw():
    print('Hello, world!')


def lines(fp):
    print(str(len(fp.readlines())))


def sent_make_dict(fp):
    sent_dict = {}
    with open(fp) as s:
        for line in s:
            a = str(line).split("\t")
            sent_dict.update({a[0]: int(a[1])})
    return sent_dict


def tweet_make_dict(fp):
    f = open(fp)
    tweet_dict = []
    for line in f:
        tweet = json.loads(line)
        if 'text' in tweet.keys():
            if tweet['lang'] == 'en':
                tweet_dict.append((tweet['text']))
    return tweet_dict


def score_calc(tweet_dict, sent_dict):
    for line in tweet_dict:
        tweet_score = 0
        for word in line.split():
            if word in sent_dict.keys():
                tweet_score += sent_dict[word]
        print(tweet_score)


def main():
    sent_file = open(sys.argv[1])
    tweet_file = open(sys.argv[2])
    hw()
    lines(sent_file)
    lines(tweet_file)

    # convert the sentiment file into a dictionary
    sent_dict = sent_make_dict(sys.argv[1])

    # convert the tweet file into a list of dictionaries
    tweet_dict = tweet_make_dict(sys.argv[2])

    # calculate sentiment score
    score_calc(tweet_dict, sent_dict)


if __name__ == '__main__':
    main()
