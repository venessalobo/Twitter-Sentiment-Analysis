import sys
import json
import string


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


def main():
    sent_file = open(sys.argv[1])
    tweet_file = open(sys.argv[2])
    hw()
    lines(sent_file)
    lines(tweet_file)

    # convert the sentiment file into a dictionary
    sent_dict = sent_make_dict(sys.argv[1])

    # convert the tweet file into a list of dictionaries
    tweet_file = open(sys.argv[2])

    # load json file as a dictionary
    for line in tweet_file:
        d = json.loads(line)
        # analyze only english tweets in the text attribute
        if 'text' in d.keys():
            if d['lang'] == 'en':
                # eliminate punctuations in the tweet
                norm_tweet = norm_word(d['text'])
                # calculate sentiment score and obtain words with no corresponding value in sentiment file
                sent_score, non_sent_words = calc_sent_score(sent_dict, norm_tweet)
                ''' calculate term sentiment for the words with no sentiment value based
                    on the sentiment score of the tweet'''
                for word in non_sent_words:
                    print(word, sent_score / float(len(norm_tweet) - len(non_sent_words)))


if __name__ == '__main__':
    main()
