import os
import re

import utils

import tqdm
from revChatGPT.V3 import Chatbot


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


def remove_quotation_marks(text: str):
    return text.replace('"', "")


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

    return curr_text


def ask_chat_gpt_warmup(chatgpt, warmup_query):
    ask_chat_gpt(chatgpt = chatgpt,
                 query = warmup_query,
                 curr_text = "",
                 continue_if_needed = False)


def generate_caption(chatgpt: Chatbot, query):
    return extract_captions(remove_quotation_marks(ask_chat_gpt(chatgpt = chatgpt,
                                                                query = query,
                                                                curr_text = "",
                                                                continue_if_needed = False)))


def extract_captions(bot_response):
    captions = []
    for l in bot_response.splitlines():
        caption = l.split(" - ")[-1]

        caption = caption.lstrip()  # removes leading whitespaces, newline and tab characters on string beginning
        caption = caption.replace("- ", "")
        caption = caption.replace(". ", "")
        caption = re.sub(r'[0-9]+', '', caption)  # removes digits from string

        captions.append(caption)

    return captions


def generate_captions_dict(chatgpt: Chatbot, inference_dict: dict, save_folder: str):
    captions_dict = {}

    dict_keys = sorted(list((inference_dict.keys())))

    step = 25

    queries = []
    start = 0
    for i in range(step, len(dict_keys), step):
        query = build_one_big_query(inference_dict = inference_dict, keys = dict_keys[start: i])
        queries.append(query)
        start += step

    start -= step
    query = build_one_big_query(inference_dict = inference_dict, keys = dict_keys[start: len(dict_keys)])
    queries.append(query)

    warmup_query1 = """
       I have a disaster images classification model that, given an image of a disaster or an incident, provides several labels for both the type of incident and the place of the incident. As an example, the output could be:

    {'incidents': ['earthquake'],
    'places': ['building outdoor']
    }

    where "incidents" and "places" describe the content of the picture. An output can contain multiple values for ‘incidents’ and ‘places’. Here’s an example of such case:

    {"places": ["ocean", "coast"],
    "incidents": ["tornado"]}


    Given this output, I want to train an NLP model for performing further tweets classification. For this purpose I have to obtain a sentence that resembles a tweet sentence given these labels. Given the example above, a possible sentence could be: "The image depicts a village affected by an earthquake"

    Another possible case is when the image doesn't contain an incident. In such case the output is this:

    {'incidents': [],
    'places': []
    }

    In this case the sentence could be "The image doesn't depict any disaster"

    The output can contain information related to the place only. Here’s an example:


    {'incidents': [],
    'places': [‘building outdoor’]
    }

    In this case the sentence could be “The image shows a building outdoor”

    Can you generate these sentences for me? Avoid introducing an emotional bias into the tweet-like caption. Can you provide a result that it is as objective as possible? It has to be informative about the image content but with a tweet-like format.

    Only generate a caption, and nothing else, given this output:

    {'incidents': ['flooded'],
    'places': ['street']}
        """
    ask_chat_gpt_warmup(chatgpt = chatgpt, warmup_query = warmup_query1)

    warmup_query2 = """Now I will provide you a list of outputs, for each of these only generate a caption, and nothing else. 
    Remember to avoid introducing an emotional bias into the tweet-like captions. Provide results that it are as objective as possible
    Do not write anything but the generated captions in the answer"""

    ask_chat_gpt_warmup(chatgpt = chatgpt, warmup_query = warmup_query2)

    end = 0

    for idx, query in enumerate(tqdm.tqdm(queries)):
        generated_captions_dict = {}
        captions = generate_caption(chatgpt = chatgpt, query = query)
        start = end
        end += len(captions)
        for id, key in enumerate(dict_keys[start: end]):
            generated_captions_dict[key] = captions[id]

        utils.save_json_file(generated_captions_dict,
                             path = f"{save_folder}/crisismmd_generated_captions_dict_{idx + 1}.json")

    return captions_dict


def build_one_big_query(inference_dict, keys = None):
    query = "Generate captions for these outputs: \n"
    i = 0
    for im_path in keys:
        query += str(inference_dict[im_path])
        query += "\n"
        i += 1

    return query


def generate_captions_routine(crisismmd_inference_dict_path: str,
                              filtered_dict_file_path: str,
                              chat_gpt_token: str,
                              save_folder: str):
    inference_dict = utils.get_loaded_json_file(path = crisismmd_inference_dict_path)
    filtered_dict = filter_inference_dict(inference_dict = inference_dict,
                                          threshold_incidents = 0.2, thresold_places = 0.4)
    utils.save_json_file(filtered_dict, path = filtered_dict_file_path)
    chatgpt = Chatbot(api_key = chat_gpt_token, engine = 'gpt-3.5-turbo')
    generate_captions_dict(chatgpt = chatgpt, inference_dict = filtered_dict, save_folder = save_folder)


def unify_captions_dicts(folder_name: str):
    file_paths = os.listdir(folder_name)
    dicts = [utils.get_loaded_json_file(os.path.join(folder_name, fp)) for fp in file_paths]

    return utils.merge_dicts(dicts = dicts)


if __name__ == '__main__':
    crisismmd_inference_dict_path = "crisismmd_inference_dict.json"
    chat_gpt_token = "NOT GONNA TELL YOU :)"
    save_folder = 'temp'

    """generate_captions_routine(crisismmd_inference_dict_path = crisismmd_inference_dict_path,
                              filtered_dict_file_path = "crisismmd_filtered_inference_dict.json",
                              chat_gpt_token = chat_gpt_token,
                              save_folder = save_folder)"""

    d = unify_captions_dicts(folder_name = save_folder)
    utils.save_json_file(d, 'crisismmd_generated_sentences_02_04.json')
