import itertools
import socket
import sys
import time
from io import BytesIO
from typing import re

import requests
from tqdm import tqdm
from urllib3.exceptions import InsecureRequestWarning

import utils
import urllib.request
import os
import urllib3
urllib3.disable_warnings(InsecureRequestWarning)

import multiprocessing as mp
from uplink_service import UplinkService

global uplink_service
uplink_service = UplinkService()

def get_filename_format_from_url(url: str):
    return url.split('.')[-1]


def download_and_save_image_from_url(url: str, save_path: str):
    urllib.request.urlretrieve(url, save_path)

def get_image_binary_from_url(url:str):
    response = requests.get(url, timeout = 10, verify = False)
    image_data = BytesIO(response.content)
    return image_data


def save_image_to_storj_from_dataset_elem(dkey: str,
                                          dataset: dict,
                                          field_val: str,
                                          folder_name: str):
    try:
        url = dataset[dkey][field_val]
        data = get_image_binary_from_url(url = url)
        uplink_service.upload_binary_file(data = data, BUCKET_NAME = folder_name, filename = dkey)

    except Exception as e:
        pass

def get_image_filename_from_url(url: str):
    return url.split('/')[-1]


def fix_json_dataset(dict_dataset: dict,
                     new_path: str,
                     include_subfolders_path: bool = False):
    new_dict = {}
    for image_name in tqdm(dict_dataset.keys()):

        if not include_subfolders_path:
            subfolder_name = ""
        else:
            subfolder_name = image_name.split('/')[0] + "/"

        url_image_name = get_image_filename_from_url(url = dict_dataset[image_name]['url'])
        key_name = subfolder_name + url_image_name
        new_dict[key_name] = dict_dataset[image_name]

    utils.save_json_file(elem = new_dict, path = new_path)


def fix_datasets_structure(train_json_path: str,
                           val_json_path: str,
                           new_train_json_path: str,
                           new_val_json_path: str,
                           include_subfolders_path: bool = False):
    train_dict = utils.get_loaded_json_file(path = train_json_path)
    val_dict = utils.get_loaded_json_file(path = val_json_path)

    fix_json_dataset(dict_dataset = train_dict,
                     new_path = new_train_json_path,
                     include_subfolders_path = include_subfolders_path)
    fix_json_dataset(dict_dataset = val_dict,
                     new_path = new_val_json_path,
                     include_subfolders_path = include_subfolders_path)


if __name__ == '__main__':
    train_json_path = "IncidentsDataset/multi_label_train.json"
    val_json_path = "IncidentsDataset/multi_label_val.json"

    new_train_json_path = "IncidentsDataset/new_multi_label_train.json"
    new_val_json_path = "IncidentsDataset/new_multi_label_val.json"

    """# ALREADY EXECUTED
    fix_datasets_structure(train_json_path = train_json_path,
                           val_json_path = val_json_path,
                           new_train_json_path = new_train_json_path,
                           new_val_json_path = new_val_json_path,
                           include_subfolders_path = False)"""

    # train_dict = utils.get_loaded_json_file(path = new_train_json_path)
    val_dict = utils.get_loaded_json_file(path = new_val_json_path)

    images_save_folder = "../Incidents/images"

    if not os.path.exists(images_save_folder):
        os.makedirs(images_save_folder)

    start_time = time.time()

    cpu_count = mp.cpu_count()
    print(cpu_count)
    # uplink_service = UplinkService()
    storj_bucket_name = "incidents-images"
    params = zip(val_dict.keys(), itertools.repeat(val_dict), itertools.repeat('url'),
                 itertools.repeat(storj_bucket_name))

    # save_image_to_storj_from_dataset_elem(list(val_dict.keys())[0], val_dict, 'url', uplink_service, storj_bucket_name)

    with mp.Pool(cpu_count) as pool:
        try:
            r = pool.starmap(save_image_to_storj_from_dataset_elem, tqdm(params, total = len(list(val_dict.keys()))))
        except:
            pass