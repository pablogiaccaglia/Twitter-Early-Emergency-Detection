import itertools
import sys
import time
import multiprocessing as mp
import utils
from tqdm import tqdm

from urllib3.exceptions import InsecureRequestWarning
import utils
import urllib3
urllib3.disable_warnings(InsecureRequestWarning)

def save_image_to_onedrive_from_dataset_elem(dkey: str,
                                             dataset: dict,
                                             urls_field_val: str,
                                             folder_id: str,
                                             filenames_field_val: str,
                                             AT: str):
    try:
        urls = dataset[dkey][urls_field_val]
        filenames = dataset[dkey][filenames_field_val]

        for url, filename in zip(urls, filenames):
            data = utils.get_image_binary_from_url(url = url)
            utils.upload_binary_file_to_onedrive(data = data,
                                                 folder_id = folder_id,
                                                 filename = filename,
                                                 AT = AT)

    except Exception:
        pass


if __name__ == '__main__':

    crisismd_images_json_dict = "CrisisMMD_v2.0/crisismd_tweets_media_urls.json"
    ONEDRIVE_FOLDER_ID = "ONEDRIVE_FOLDER_IDE"
    AT = "ACCESS_TOKEN"
    data_dict = utils.get_loaded_json_file(path = crisismd_images_json_dict)

    start_time = time.time()

    cpu_count = mp.cpu_count()
    print("CPU COUNT" + str(cpu_count))
    params = zip(data_dict.keys(),
                 itertools.repeat(data_dict),
                 itertools.repeat('urls'),
                 itertools.repeat(ONEDRIVE_FOLDER_ID),
                 itertools.repeat('filenames'),
                 itertools.repeat(AT))

    with mp.Pool(cpu_count) as pool:
        try:
            r = pool.starmap(save_image_to_onedrive_from_dataset_elem,
                             tqdm(params, total = len(list(data_dict.keys()))))
        except:
            pass
