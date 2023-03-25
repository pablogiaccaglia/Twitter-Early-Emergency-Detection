import time
from datetime import datetime

from pandas import DataFrame
from snscrape.modules.twitter import Tweet
from snscrape.modules.twitter import TwitterTweetScraperMode
from snscrape.modules.twitter import _TwitterAPIScraper
from snscrape.modules.twitter import _TwitterAPIType
import pandas as pd
import json
import multiprocessing as mp

def txt_to_list(filename: str):
    with open(filename) as file:
        lines = list(set([line.rstrip() for line in file]))
    return lines


def parse_twitter_media_content(tweet: Tweet):
    if tweet.media:
        return [m.fullUrl for m in tweet.media]
    else:
        return None


def get_tweet_by_id(tweet_id):
    # Creating list to append tweet data
    try:
        tweet = list(TwitterTweetScraper(tweetId = tweet_id).get_items())
        tweet = tweet[0]
        return [tweet.date,
                tweet.id,
                tweet.rawContent,
                tweet.renderedContent,
                tweet.user.username,
                tweet.replyCount,
                tweet.retweetCount,
                tweet.likeCount,
                tweet.quoteCount,
                tweet.viewCount,
                tweet.hashtags,
                tweet.media,
                tweet.coordinates,
                tweet.place]
    except:
        pass

    return None


def build_tweets_csv(tweets_ids, csv_filename):
    start_time = time.time()

    cpu_count = mp.cpu_count()
    pool = mp.Pool(cpu_count)
    tweets = pool.map(get_tweet_by_id, tweets_ids)

    pool.close()
    pool.join()

    print("--- %s seconds ---" % (time.time() - start_time))

    tweets_list = [tweet for tweet in tweets if tweet is not None]
    # Creating a dataframe from the tweets list above
    tweets_df = pd.DataFrame(tweets_list, columns = ['Datetime',
                                                     'Tweet Id',
                                                     'Raw content',
                                                     'Text',
                                                     'Username',
                                                     'Reply Count',
                                                     'Retweet Count',
                                                     'Like Count',
                                                     'Quote Count',
                                                     'View Count',
                                                     'Hashtags',
                                                     'Media',
                                                     'Coordinates',
                                                     'Place'])

    tweets_df.to_csv(csv_filename)


def get_tweets_ids_from_kaggle_dataset(Kaggle_dataset_filename: str,
                                       start_date = None,
                                       end_date = None):
    Kaggle_dataset_filename = Kaggle_dataset_filename
    column_types = {
        'ID':       str,
        'Time':     str,
        'Tweet':    str,
        'Retweets': "Int64",
        'Replies':  "Int64",
        'Likes':    "Int64"
    }

    Kaggle_df = pd.read_csv(Kaggle_dataset_filename, header = 0, dtype = column_types)
    Kaggle_df = Kaggle_df.dropna()
    Kaggle_df = Kaggle_df.reset_index(drop = True)

    if start_date and end_date:
        Kaggle_df['Time'] = pd.to_datetime(Kaggle_df['Time'], format = "%Y-%m-%d %H:%M:%S")
        Kaggle_df = slice_kaggle_dataframe_by_date(dataframe = Kaggle_df,
                                                   date_column_name = "Time",
                                                   start_date = start_date,
                                                   end_date = end_date)

    Kaggle_tweets_ids = get_csv_column(dataframe = Kaggle_df, columnName = 'ID')
    Kaggle_tweets_ids = list(set([tweet_id for tweet_id in Kaggle_tweets_ids if tweet_id.isdigit()]))  # 46099 tweet ids

    return Kaggle_tweets_ids


def get_csv_column(dataframe: DataFrame, columnName: str):
    column_names = list(dataframe.columns)

    if columnName in column_names:
        return dataframe[columnName].values.tolist()
    else:
        raise NameError("Column name doesn't exist")


def get_tweets_ids_from_crisismmd_dataset(
        CrisisMMD_datset_filename: str,
        start_date: datetime = None,
        end_date: datetime = None
):
    CrisisMMD_dataset_ids = []

    "Sun Sep 03 17:37:13 +0000 2017"
    with open(CrisisMMD_datset_filename, 'r') as f:
        for line in f:
            try:
                tweet = json.loads(line)
                date = datetime.strptime(tweet['created_at'], '%a %b %d %H:%M:%S +0000 %Y')

                if start_date and end_date:
                    if start_date <= date <= end_date:
                        CrisisMMD_dataset_ids.append(tweet['id_str'])
                else:
                    CrisisMMD_dataset_ids.append(tweet['id_str'])

            except json.decoder.JSONDecodeError:
                pass  # skip this line
    return CrisisMMD_dataset_ids


def slice_kaggle_dataframe_by_date(dataframe: DataFrame, date_column_name: str, start_date: datetime,
                                   end_date: datetime):
    mask = (dataframe[date_column_name] >= start_date) & (dataframe[date_column_name] <= end_date)
    return dataframe.loc[mask]


class TwitterTweetScraper(_TwitterAPIScraper):
    name = 'twitter-tweet'

    def __init__(self, tweetId, *, mode = TwitterTweetScraperMode.SINGLE, **kwargs):
        self._tweetId = tweetId
        self._mode = mode
        super().__init__(f'https://twitter.com/i/web/status/{self._tweetId}', **kwargs)

    def get_items(self):
        paginationVariables = {
            'focalTweetId':                           str(self._tweetId),
            'cursor':                                 None,
            'referrer':                               'tweet',
            'with_rux_injections':                    False,
            'includePromotedContent':                 True,
            'withCommunity':                          True,
            'withQuickPromoteEligibilityTweetFields': True,
            'withBirdwatchNotes':                     False,
            'withSuperFollowsUserFields':             True,
            'withDownvotePerspective':                False,
            'withReactionsMetadata':                  False,
            'withReactionsPerspective':               False,
            'withSuperFollowsTweetFields':            True,
            'withVoice':                              True,
            'withV2Timeline':                         True,
        }
        variables = paginationVariables.copy()
        del variables['cursor'], variables['referrer']
        features = {
            'responsive_web_twitter_blue_verified_badge_is_enabled':                   True,
            'responsive_web_graphql_exclude_directive_enabled':                        False,
            'verified_phone_label_enabled':                                            False,
            'responsive_web_graphql_timeline_navigation_enabled':                      True,
            'responsive_web_graphql_skip_user_profile_image_extensions_enabled':       False,
            'tweetypie_unmention_optimization_enabled':                                True,
            'vibe_api_enabled':                                                        True,
            'responsive_web_edit_tweet_api_enabled':                                   True,
            'graphql_is_translatable_rweb_tweet_is_translatable_enabled':              True,
            'view_counts_everywhere_api_enabled':                                      True,
            'longform_notetweets_consumption_enabled':                                 True,
            'tweet_awards_web_tipping_enabled':                                        False,
            'freedom_of_speech_not_reach_fetch_enabled':                               False,
            'standardized_nudges_misinfo':                                             True,
            'tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled': False,
            'interactive_text_enabled':                                                True,
            'responsive_web_text_conversations_enabled':                               False,
            'responsive_web_enhance_cards_enabled':                                    False,
        }

        params = {'variables': variables, 'features': features}
        url = 'https://twitter.com/i/api/graphql/NNiD2K-nEYUfXlMwGCocMQ/TweetDetail'
        obj = self._get_api_data(url, _TwitterAPIType.GRAPHQL, params = params)
        if not obj['data']:
            return
        for instruction in obj['data']['threaded_conversation_with_injections_v2']['instructions']:
            if instruction['type'] != 'TimelineAddEntries':
                continue
            for entry in instruction['entries']:
                if entry['entryId'] == f'tweet-{self._tweetId}' and entry['content'][
                    'entryType'] == 'TimelineTimelineItem' and entry['content']['itemContent'][
                    'itemType'] == 'TimelineTweet':
                    yield self._graphql_timeline_tweet_item_result_to_tweet(
                            entry['content']['itemContent']['tweet_results']['result'], tweetId = self._tweetId)

