import itertools
import socket
import time

from tqdm import tqdm
import utils
import urllib.request
import os
import istarmap
import multiprocessing as mp


def get_filename_format_from_url(url: str):
    return url.split('.')[-1]


def download_and_save_image_from_url(url: str, save_path: str):
    urllib.request.urlretrieve(url, save_path)


def save_image_from_dataset_elem(dkey: str, dataset: dict, field_val: str, save_folder: str):
    url = dataset[dkey][field_val]
    try:

        save_path = save_folder + '/' + dkey
        save_subfolder = "".join([elem + '/' for elem in save_path.split('/')[:-1]])
        if not os.path.exists(save_subfolder):
            os.makedirs(save_subfolder)

        download_and_save_image_from_url(url = url, save_path = save_path)
    except:
        pass


def get_image_filename_from_url(url: str):
    return url.split('/')[-1]


def fix_json_dataset(dict_dataset: dict, new_path: str):
    new_dict = {}
    for image_name in tqdm(dict_dataset.keys()):
        subfolder_name = image_name.split('/')[0]
        url_image_name = get_image_filename_from_url(url = dict_dataset[image_name]['url'])
        key_name = subfolder_name + '/' + url_image_name
        new_dict[key_name] = dict_dataset[image_name]

    utils.save_json_file(elem = new_dict, path = new_path)


def fix_datasets_structure(train_json_path: str,
                           val_json_path: str,
                           new_train_json_path: str,
                           new_val_json_path: str):
    train_dict = utils.get_loaded_json_file(path = train_json_path)
    val_dict = utils.get_loaded_json_file(path = val_json_path)

    fix_json_dataset(dict_dataset = train_dict, new_path = new_train_json_path)
    fix_json_dataset(dict_dataset = val_dict, new_path = new_val_json_path)


if __name__ == '__main__':
    train_json_path = "IncidentsDataset/multi_label_train.json"
    val_json_path = "IncidentsDataset/multi_label_val.json"

    new_train_json_path = "IncidentsDataset/new_multi_label_train.json"
    new_val_json_path = "IncidentsDataset/new_multi_label_val.json"

    # ALREADY EXECUTED
    """fix_datasets_structure(train_json_path = train_json_path,
                           val_json_path = val_json_path,
                           new_train_json_path = new_train_json_path,
                           new_val_json_path = new_val_json_path)"""

    train_dict = utils.get_loaded_json_file(path = new_train_json_path)
    val_dict = utils.get_loaded_json_file(path = new_val_json_path)

    images_save_folder = "/Users/pablo/Desktop/MDP/Incidents/images"

    if not os.path.exists(images_save_folder):
        os.makedirs(images_save_folder)

    start_time = time.time()

    cpu_count = mp.cpu_count()
    params = zip(train_dict.keys(), itertools.repeat(train_dict), itertools.repeat('url'),
                 itertools.repeat(images_save_folder))
    with mp.Pool(cpu_count) as pool:
        # results = pool.starmap(save_image_from_dataset_elem, tqdm(params, total = len(params)))

        for _ in tqdm(pool.istarmap(save_image_from_dataset_elem, params),
                      total = len(list(train_dict.keys()))):
            pass

    pool.close()
    pool.join()
