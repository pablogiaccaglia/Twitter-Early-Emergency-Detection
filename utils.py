import sys
import time
import urllib
from datetime import datetime
from io import BytesIO
import requests
from pandas import DataFrame
from snscrape.modules.twitter import Tweet
import pandas as pd
import json
from p_tqdm import p_map
from snscrape.modules.twitter import TwitterTweetScraper
import re
import ast

from uplink_service import UplinkService

def get_filename_format_from_url(url: str):
    return url.split('/')[-1]

def save_json_file(elem, path):
    with open(path, "w") as fp:
        json.dump(elem, fp)

def get_loaded_json_file(path):
    with open(path, "r") as fp:
        return json.load(fp)
def download_and_save_image_from_url(url: str, save_path: str):
    urllib.request.urlretrieve(url, save_path)

def get_image_binary_from_url(url:str):
    response = requests.get(url, timeout = 10, verify = False)
    image_data = BytesIO(response.content)
    return image_data
def upload_binary_file_to_onedrive(
        data,
        folder_id,
        AT,
        filename
):
    GRAPH_API_ENDPOINT = 'https://graph.microsoft.com/v1.0/'
    auth = 'Bearer ' + AT
    headers = {'Authorization': auth}
    response = requests.put(
            url = GRAPH_API_ENDPOINT + f"users/32bb8e68-0b17-4a83-acd7-06db6015d8a0/drive/items/{folder_id}:/{filename}:/content",
            headers = headers,
            data = data
    )

    return response


def txt_to_list(filename: str):
    with open(filename) as file:
        lines = list(set([int(line.rstrip()) for line in file]))
        lines.sort()
        lines = [str(line) for line in lines]
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
                parse_twitter_media_content(tweet),
                tweet.coordinates,
                tweet.place]
    except:
        pass

    return None


def build_tweets_csv(tweets_ids, csv_filename):
    start_time = time.time()

    tweets = p_map(get_tweet_by_id, tweets_ids)

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
                pass
    return CrisisMMD_dataset_ids


def merge_dicts(dicts:list):
    merged = dict()

    for d in dicts:
        for k, v in d.items():  # use d.iteritems() in python 2
            merged[k] = v

    return merged

def slice_kaggle_dataframe_by_date(dataframe: DataFrame, date_column_name: str, start_date: datetime,
                                   end_date: datetime):
    mask = (dataframe[date_column_name] >= start_date) & (dataframe[date_column_name] <= end_date)
    return dataframe.loc[mask]


def get_url_from_csv_cell(cell_content:str):
    return re.findall('.\'([^\']*)\'.', cell_content)[-1]

def build_media_dict_from_df(df:DataFrame, media_column_name:str, text_column_name:str):
    df = df[df[media_column_name].notnull()]
    d = {}

    # could parallelize this through Pool Map
    for index, row in df.iterrows():
        url = get_url_from_csv_cell(cell_content = row[media_column_name])
        d[row[text_column_name]] = url
    return d

def get_filename_from_twitter_media_url(url:str):
    name = re.search('.media/([^\']*)\?.', url).group(1)

    extension = re.search('.format=([^\']*)&.', url).group(1)

    return name + "." + extension


def save_image_to_storj_from_media_dict_elem(dkey: str,
                                             dataset: dict,
                                             url_field_name: str,
                                             folder_name: str):
    try:
        uplink_service = UplinkService()
        url = dataset[dkey][url_field_name]
        data = get_image_binary_from_url(url = url)
        filename = get_filename_from_twitter_media_url(url = url)
        uplink_service.upload_binary_file(data = data, BUCKET_NAME = folder_name, filename = filename)
        dataset[dkey][url_field_name] = filename
    except Exception as e:
        print(e)
        sys.stdout.flush()
        dataset[dkey][url_field_name] = None


def fix_media_field(entry):
    def get_url_from_csv_cell(cell_content: str):
        return re.findall('.\'([^\']*)name=orig\'.', cell_content)[-1] + "name=orig"

    def get_url_from_csv_cell_2(cell_content: str):
        return re.findall('.\'([^\']*).jpg\'.', cell_content)[-1] + ".jpg"

    def get_url_from_csv_cell_3(cell_content: str):
        return re.findall('.\'([^\']*).png\'.', cell_content)[-1] + ".png"

    if not isinstance(entry, str):
        return entry
    try:
        urls = ast.literal_eval(entry)
    except:
        try:
            urls = [get_url_from_csv_cell(entry)]
        except:
            try:
                urls = [get_url_from_csv_cell_2(entry)]
            except:
                urls = [get_url_from_csv_cell_3(entry)]

    return urls
