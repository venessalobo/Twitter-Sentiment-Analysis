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
    for word in line.split(' '):
        if word in sent_dict:
            sent_score += sent_dict[word]
    return sent_score


def geo_info(tweet):
    try:
        if tweet['place']['country_code'] == 'US':
            state = tweet['place']['full_name'][-2:]
            states = {
                'AK': 'Alaska',
                'AL': 'Alabama',
                'AR': 'Arkansas',
                'AS': 'American Samoa',
                'AZ': 'Arizona',
                'CA': 'California',
                'CO': 'Colorado',
                'CT': 'Connecticut',
                'DC': 'District of Columbia',
                'DE': 'Delaware',
                'FL': 'Florida',
                'GA': 'Georgia',
                'GU': 'Guam',
                'HI': 'Hawaii',
                'IA': 'Iowa',
                'ID': 'Idaho',
                'IL': 'Illinois',
                'IN': 'Indiana',
                'KS': 'Kansas',
                'KY': 'Kentucky',
                'LA': 'Louisiana',
                'MA': 'Massachusetts',
                'MD': 'Maryland',
                'ME': 'Maine',
                'MI': 'Michigan',
                'MN': 'Minnesota',
                'MO': 'Missouri',
                'MP': 'Northern Mariana Islands',
                'MS': 'Mississippi',
                'MT': 'Montana',
                'NA': 'National',
                'NC': 'North Carolina',
                'ND': 'North Dakota',
                'NE': 'Nebraska',
                'NH': 'New Hampshire',
                'NJ': 'New Jersey',
                'NM': 'New Mexico',
                'NV': 'Nevada',
                'NY': 'New York',
                'OH': 'Ohio',
                'OK': 'Oklahoma',
                'OR': 'Oregon',
                'PA': 'Pennsylvania',
                'PR': 'Puerto Rico',
                'RI': 'Rhode Island',
                'SC': 'South Carolina',
                'SD': 'South Dakota',
                'TN': 'Tennessee',
                'TX': 'Texas',
                'UT': 'Utah',
                'VA': 'Virginia',
                'VI': 'Virgin Islands',
                'VT': 'Vermont',
                'WA': 'Washington',
                'WI': 'Wisconsin',
                'WV': 'West Virginia',
                'WY': 'Wyoming'
            }
            if state in states.keys():
                return True, state
        else:
            return False, ''
    except:
        pass
    return False, ''


def main():
    sent_dict = sent_make_dict(sys.argv[1])
    tweet_file = open(sys.argv[2])

    # initialize empty dict
    state_happy_index = defaultdict()
    # initialize counter
    total_tweet_cnt = 0

    # load json file as a dictionary
    for line in tweet_file:
        d = json.loads(line)
        # try module analyzes tweets with country code = 'US' else the tweet is passed into the except block
        try:
            # analyze only english tweets in the text attribute
            if d['lang'] == 'en':
                if 'text' in d.keys():
                    # eliminate punctuations
                    norm_tweet = norm_word(d['text'])
                    # obtain state code
                    is_usa, state = geo_info(d)
                    if is_usa:
                        total_tweet_cnt += 1
                        # calculate the sentiment score of the tweet
                        sent_score = calc_sent_score(sent_dict, norm_tweet)
                        if state in state_happy_index:
                            state_happy_index[state] += sent_score
                        else:
                            state_happy_index[state] = sent_score
        except:
            pass

    # initialize dummy state and score
    happiest_state = ''
    happiest_state_score = 0

    # select the state with the highest score
    for state, score in state_happy_index.items():
        if score > happiest_state_score:
            happiest_state_score = score
            happiest_state = state
    print(happiest_state)


if __name__ == '__main__':
    main()