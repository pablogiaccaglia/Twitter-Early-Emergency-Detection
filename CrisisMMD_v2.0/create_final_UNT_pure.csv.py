from datetime import datetime

import pandas as pd
import json
import utils


def build_hashtags_list(tweet_dict):
    hashtags = []

    for entry in tweet_dict['entities']['hashtags']:
        hashtags.append(entry['text'])

    return hashtags

def build_media_list(tweet_dict):
    urls = []

    if 'extended_entities' in tweet_dict:
        for entry in tweet_dict['extended_entities']['media']:
            urls.append(entry['media_url'])
    else:
        for entry in tweet_dict['extended_tweet']['extended_entities']['media']:
            urls.append(entry['media_url'])

    return urls


def build_dict_adapt(path, csv_to_extend):
    tweets_ids = sorted(list(csv_to_extend['Tweet Id']))

    start_idx = csv_to_extend.iloc[-1, [0]][0] + 1

    with open(path, 'r') as f:
        for line in f:
            tweet = json.loads(line)

            if tweet['id'] in tweets_ids and not csv_to_extend.loc[csv_to_extend['Tweet Id'] == tweet['id']]['Media'].isnull().all():
                continue
            else:

                if tweet['id'] in tweets_ids and csv_to_extend.loc[csv_to_extend['Tweet Id'] == tweet['id']]['Media'].isnull().all():
                    l = build_media_list(tweet)
                    csv_to_extend.loc[csv_to_extend['Tweet Id'] == tweet['id'], 'Media'] = str(l)

                else:

                    date = datetime.strptime(tweet['created_at'], '%a %b %d %H:%M:%S +0000 %Y')
                    entry = {
                        'Idx': start_idx,
                        'Datetime':      date,
                        'Tweet Id':      tweet['id'],
                        'Raw content':    tweet['text'],
                        'Text':          tweet['text'],
                        'Username':      tweet['user']['screen_name'],
                        'Reply Count':   None,
                        'Retweet Count': tweet['retweet_count'],
                        'Like Count':    None,
                        'Quote Count':   None,
                        'View Count':    None,
                        'Hashtags':      build_hashtags_list(tweet),
                        'Media':         build_media_list(tweet),
                        'Coordinates':   None,
                        'Place':         None
                    }

                    start_idx +=1

                    csv_to_extend = csv_to_extend.append(entry, ignore_index = True)

    return csv_to_extend


dtypes = {
    'Unnamed':       "Int64",
    'Datetime':      object,
    'Tweet Id':      "Int64",
    'Raw content':   str,
    'Text':          str,
    'Username':      str,
    'Reply Count':   "Int16",
    'Retweet Count': "Int16",
    'Like Count':    "Int16",
    'Quote Count':   "Int16",
    'View Count':    "Int16",
    'Hashtags':      object,
    'Media':         object,
    'Coordinates':   object,
    'Place':         object

}

scraped_csv = pd.read_csv("CrisisMMD_scraped_dataset.csv", dtype = dtypes)

dict2 = build_dict_adapt("json/hurricane_harvey_final_data.json", scraped_csv)

print(dict2.info())

dict2.to_csv("CrisisMMD_final_dataset_full.csv")

#labels = pd.read_csv("hurricane_harvey_final_data.tsv", sep = '\t')


