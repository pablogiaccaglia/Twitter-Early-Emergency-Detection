import ast
import pandas as pd
from nltk import WordNetLemmatizer
import os
import re
from nltk import LancasterStemmer
from nltk.corpus import stopwords
import contractions
import inflect
import utils
import tqdm
from revChatGPT.V3 import Chatbot


def remove_emoji(text):
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               u"\U00002702-\U000027B0"
                               u"\U000024C2-\U0001F251"
                               "]+", flags = re.UNICODE)
    return emoji_pattern.sub(r'', text)


def replace_contractions(text):
    """Replace contractions in string of text"""
    return contractions.fix(text)


def remove_URL(sample):
    """Remove URLs from a sample string"""
    s = re.sub(r'\b(?:\w+(?:[-.]\w+)*\.)+\w*(?:[-./]\w*)*(?:/|\b)', '', sample)
    s = re.sub(
        r'https?://\S+|www\.\S+|bit\.ly/\S+|t\.co/\S+|ow\.ly/\S+|tinyurl\.com/\S+|is\.gd/\S+|goo\.gl/\S+|ow\.ly/\S+|buff\.ly/\S+|adf\.ly/\S+|ift\.tt/\S+',
        " ", s)

    s = re.sub(r"http\S+", "", s)

    return s


def remove_HTML(text):
    return re.sub('r<.*?>', ' ', text)


def remove_mentions(text):
    return re.sub(r'@\w+', ' ', text)


def remove_multiple_spaces(text):
    return re.sub('\s+', ' ', text)


def remove_RT(words):
    w = words.replace("RT : ", "")
    w = w.replace("rt : ", "")
    w = w.replace(" rt ", "")
    return w


def remove_amp(words):
    w = words.replace("&amp;", "")
    w = w.replace("&lt;", "")
    w = w.replace("&gt;", "")
    w = re.sub('r&.*?;', '', w)
    return w.replace(" amp ", "")


def remove_dash(words):
    return words.replace(" - ", "")


def remove_non_ascii(text, remove_emoji = True):
    # Pattern to match emojis
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               "]+", flags = re.UNICODE)

    # print([c for c in text])
    if remove_emoji:
        text = ''.join(c for c in text if c.isascii())
    else:  # Remove non-ASCII characters except emojis
        text = ''.join(c for c in text if c.isascii() or emoji_pattern.match(c))

    return text


def to_lowercase(words):
    """Convert all characters to lowercase from list of tokenized words"""
    new_words = []
    for word in words:
        new_word = word.lower()
        new_words.append(new_word)
    return new_words


def remove_punctuation(words):
    """Remove punctuation from list of tokenized words"""
    new_words = []
    for word in words:
        new_word = re.sub(r'[^\w\s]', '', word)
        if new_word != '':
            new_words.append(new_word)
    return new_words


def replace_numbers(words):
    """Replace all interger occurrences in list of tokenized words with textual representation"""
    p = inflect.engine()
    new_words = []
    for word in words:
        if word.isdigit():
            new_word = p.number_to_words(word)
            new_words.append(new_word)
        else:
            new_words.append(word)
    return new_words


def remove_stopwords(words):
    """Remove stop words from list of tokenized words"""
    new_words = []
    for word in words:
        if word not in stopwords.words('english'):
            new_words.append(word)
    return new_words


def stem_words(words):
    """Stem words in list of tokenized words"""
    stemmer = LancasterStemmer()
    stems = []
    for word in words:
        stem = stemmer.stem(word)
        stems.append(stem)
    return stems


def lemmatize_verbs(words):
    """Lemmatize verbs in list of tokenized words"""
    lemmatizer = WordNetLemmatizer()
    lemmas = []
    for word in words:
        lemma = lemmatizer.lemmatize(word, pos = 'v')
        lemmas.append(lemma)
    return lemmas


def normalize(words):
    words = to_lowercase(words)
    words = remove_punctuation(words)
    words = remove_stopwords(words)
    return words


def convert_space(text):
    text = text.replace(u'\xa0', u' ')
    return text


def remove_harvey(text):
    text = text.replace("harvey ", "")
    text = text.replace("Harvey ", "")
    return text


def remove_newlines(text):
    text = re.sub('\n', ' ', text)
    return text


def clean_tweet(sample):
    if isinstance(sample, float):
        return sample
    sample = convert_space(sample)
    sample = remove_multiple_spaces(sample)
    sample = remove_newlines(sample)
    sample = remove_URL(sample)
    sample = remove_HTML(sample)
    sample = remove_mentions(sample)
    sample = remove_dash(sample)
    sample = remove_amp(sample)
    sample = remove_non_ascii(sample, remove_emoji = False)
    # sample = remove_harvey(sample)
    sample = replace_contractions(sample)
    sample = remove_multiple_spaces(sample)
    sample = remove_RT(sample)
    return sample


def filter_inference_dict(inference_dict: dict,
                          threshold_incidents: float = 0.5,
                          thresold_places: float = 0.5):
    filtered_dict = {}
    for im_path in inference_dict:
        details = inference_dict[im_path]

        incidents = details['incidents']
        places = details['places']
        incident_probs = details['incident_probs']
        place_probs = details['place_probs']

        filtered_incidents = []
        filtered_places = []

        for incident, incident_prob in zip(incidents, incident_probs):

            if incident_prob > threshold_incidents:
                filtered_incidents.append(incident)

        for place, place_prob in zip(places, place_probs):
            if place_prob > thresold_places:
                filtered_places.append(place)

        filtered_dict[im_path] = {
            'places':    filtered_places,
            'incidents': filtered_incidents
        }

    return filtered_dict


def ask_chat_gpt(chatgpt, query, curr_text, continue_if_needed = True):
    prev_text = chatgpt.ask(
            query
    )

    curr_text += prev_text

    if prev_text[-1] != '.' and continue_if_needed:
        prev_text = chatgpt.ask(
                "Continue"
        )
        curr_text = curr_text[:-1] + prev_text[1:]

    print(curr_text)
    return curr_text


def ask_chat_gpt_warmup(chatgpt, warmup_query):
    ask_chat_gpt(chatgpt = chatgpt,
                 query = warmup_query,
                 curr_text = "",
                 continue_if_needed = False)


def build_generated_tweets_dict(strings_list, ids):
    d = {}

    for i, elem in enumerate(strings_list):
        d[ids[i]] = elem

    return d


def generate_tweets(chatgpt: Chatbot, query, ids):
    strings_list = extract_tweets(ask_chat_gpt(chatgpt = chatgpt,
                                               query = query,
                                               curr_text = "",
                                               continue_if_needed = False))

    return build_generated_tweets_dict(strings_list = strings_list, ids = ids)


def extract_tweets(bot_response):
    marker = "```"
    bot_response = bot_response.split(marker)[1].split(marker)[0]
    bot_response = bot_response.replace("# INFORMATIVE TWEETS", "")
    bot_response = bot_response.replace("- INFORMATIVE", "")
    bot_response = bot_response.replace("- NOT INFORMATIVE", "")
    bot_response = bot_response.replace("# NOT INFORMATIVE TWEETS", "")

    strings_list = ast.literal_eval(bot_response)
    return strings_list


def generate_tweets_dict(chatgpt: Chatbot, inference_dict: dict, save_folder: str):
    captions_dict = {}

    dict_keys = sorted(list((inference_dict.keys())))

    step = 10

    queries = {}
    start = 0
    for i in range(step, len(dict_keys), step):
        query = build_one_big_query(inference_dict = inference_dict, keys = dict_keys[start: i])
        queries[i] = {
            "ids":   dict_keys[start: i],
            'query': query
        }

        start += step

    start -= step
    query = build_one_big_query(inference_dict = inference_dict, keys = dict_keys[start: len(dict_keys)])
    queries[i] = {
        "ids":   dict_keys[start: len(dict_keys)],
        'query': query
    }

    print(i)
    print(len(dict_keys))

    warmup_query1 = """I need to perform text augmentation for training a Bert model for tweets classification of  relevant and not relevant tweets related to hurricane harvey dataset,
The purpose of this task is to determine whether a given tweet or image, which was collected during the Hurricane Harvey of 2017, is useful for humanitarian aid purposes as defined below. If the given tweet is useful for humanitarian aid, it is
considered as an “Informative” tweet/image, otherwise as a
“Not informative” tweet.
“Humanitarian aid” definition: In response to humanitarian crises including natural and man-made disasters, humanitarian aid involves providing assistance to people who
need help. The primary purpose of humanitarian aid is to
save lives, reduce suffering, and rebuild affected communities. Among the people in need belong homeless, refugees,
and victims of natural disasters, wars, and conflicts who
need basic necessities like food, water, shelter, medical assistance, and damage-free critical infrastructure and utilities such as roads, bridges, power-lines, and communication
poles.

Given the definition of "informative" and "not informative" tweets, I want you to provide me useful text augmentations.  Given a tweet and it's class,  rephrase the tweet into multiple conceptually similar but semantically different samples, providing me the couples (augmented tweet, class).

Here's an example of an INFORMATIVE tweet:

"BEYOND HEROES: s Fire Marshal Montgomery Chief Royall working to coordinate high water rescues."

Here's another example of INFORMATIVE tweet:

Tornado hit Daytona airport. #DaytonaBeach #hurricaneimra #Irma #airport #dab #Daytona The image attached to the tweet depicts the damage to the airport
    """
    ask_chat_gpt_warmup(chatgpt = chatgpt, warmup_query = warmup_query1)

    warmup_query2 = """now I'LL provide you a sequence of labels-tweets and you will provide me a python list of lists with the augmented tweets, YOU need to generate 2 tweets for each provided tweet, okay?
    This means that i want a PYTHON LIST where each element is a LIST of 2 generated tweets
    Just generate the list an nothing else"""

    ask_chat_gpt_warmup(chatgpt = chatgpt, warmup_query = warmup_query2)
    i = 0
    for key, elem in tqdm.tqdm(queries.items()):
        if i > 398:
            tweets_dict = generate_tweets(chatgpt = chatgpt, query = elem['query'], ids = elem['ids'])
            utils.save_json_file(tweets_dict,
                                 path = f"{save_folder}/crisismmd_sintetic_tweets_dict_{i + 1}.json")
        i += 1

    return captions_dict


def build_one_big_query(inference_dict, keys = None):
    query = ""
    i = 0
    for tweet_id in keys:
        query += inference_dict[tweet_id]['Label'] + "\n"
        query += str(inference_dict[tweet_id]['Text'])
        query += "\n--------"
        query += "\n"
        i += 1

    return query


def length(text):
    '''a function which returns the length of text'''
    return len(text)


labels_df = pd.read_csv("hurricane_harvey_final_data.tsv", sep = '\t')


def assign_target(tweet_id):
    t_info = list(labels_df.loc[labels_df['tweet_id'] == tweet_id]['text_info'])[0]

    if t_info == "informative":
        return 1
    else:
        return 0


def generate_captions_routine(crisismmd_dataset_path: str,
                              dataset_csv_dtypes,
                              crisismmd_dict_file_path: str,
                              chat_gpt_token: str,
                              save_folder: str):
    pd_dataset = pd.read_csv(crisismmd_dataset_path, dtype = dataset_csv_dtypes)
    pd_dataset['length'] = pd_dataset['Text'].apply(length)
    pd_dataset['text_info'] = pd_dataset['Tweet Id'].apply(assign_target)

    pd_dataset['Ext Text'] = pd_dataset['Ext Text'].apply(lambda x: clean_tweet(x))

    tweets_dict = prepare_tweets_dict(pd_dataset = pd_dataset)

    utils.save_json_file(tweets_dict, path = crisismmd_dict_file_path)
    chatgpt = Chatbot(api_key = chat_gpt_token, engine = 'gpt-3.5-turbo-0301')
    generate_tweets_dict(chatgpt = chatgpt, inference_dict = tweets_dict, save_folder = save_folder)


def unify_captions_dicts(folder_name: str):
    file_paths = os.listdir(folder_name)
    dicts = [utils.get_loaded_json_file(os.path.join(folder_name, fp)) for fp in file_paths]

    return utils.merge_dicts(dicts = dicts)


def prepare_tweets_dict(pd_dataset):
    tweets_dict = {}
    for idx, row in pd_dataset.iterrows():
        tweets_dict[row['Tweet Id']] = {
            'Text':  row['Ext Text'],
            'Label': "INFORMATIVE TWEET" if row['text_info'] == 1 else "NOT INFORMATIVE TWEET"
        }

    return tweets_dict


if __name__ == '__main__':
    save_folder = 'temp'
    crisismmd_dataset_path = "CrisisMMD_final_dataset_captions.csv"

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
        'Place':         object,
        'Captions':      object,
        'Ext Text':      object

    }

    chat_gpt_token = "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"

    generate_captions_routine(crisismmd_dataset_path = crisismmd_dataset_path,
                              dataset_csv_dtypes = dtypes,
                              crisismmd_dict_file_path = "crisismmd_dataset_dict.json",
                              chat_gpt_token = chat_gpt_token,
                              save_folder = save_folder)

    d = unify_captions_dicts(folder_name = save_folder)
    utils.save_json_file(d, 'crisismmd_generated_tweets.json')
