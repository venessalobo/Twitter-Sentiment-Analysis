import sys
import json
import string
from collections import defaultdict
import operator


def norm_word(word):
    exclude = set(string.punctuation)
    word = ''.join(ch for ch in word.lower() if ch not in exclude)
    return word


def update_dict(h_tags, hashtag_dict):
    for hashtag in h_tags:
        if hashtag in hashtag_dict:
            hashtag_dict[hashtag] += 1
        else:
            hashtag_dict[hashtag] = 1


def main():
    tweet_file = open(sys.argv[1])

    # initialize default dict
    hashtag_dict = defaultdict()
    for line in tweet_file:
        # load json file as a dictionary
        d = json.loads(line)
        try:
            # analyze only english tweets
            if d['lang'] == 'en':
                hashtags = d['entities']['hashtags']
                h_tags = []
                # make a list of hashtags in each tweet
                for tags in hashtags:
                    h_tags.append(norm_word(tags['text']))
                # update the dict with the frequency of hashtags
                update_dict(h_tags, hashtag_dict)

        except:
            pass
    hashtag_dict = sorted(hashtag_dict.items(), key=operator.itemgetter(1), reverse=True)
    # top ten hashtags
    for i in hashtag_dict[:10]:
        print(i)


if __name__ == '__main__':
    main()