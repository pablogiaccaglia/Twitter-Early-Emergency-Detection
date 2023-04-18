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

    except Exception as e:
        pass


if __name__ == '__main__':

    kaggle_images_json_dict = "UNT_tweets_media_urls.json"
    ONEDRIVE_FOLDER_ID = "01NU2AK4S4ID2OOM3LPRAYMM6KB6O3JDCP"
    AT = "eyJ0eXAiOiJKV1QiLCJub25jZSI6Ik5PNXJHYmV4cG5vc2ZwVG50WTZDTjFPUFdwUXBJVzNvX1paV2IwdGVXZWMiLCJhbGciOiJSUzI1NiIsIng1dCI6Ii1LSTNROW5OUjdiUm9meG1lWm9YcWJIWkdldyIsImtpZCI6Ii1LSTNROW5OUjdiUm9meG1lWm9YcWJIWkdldyJ9.eyJhdWQiOiIwMDAwMDAwMy0wMDAwLTAwMDAtYzAwMC0wMDAwMDAwMDAwMDAiLCJpc3MiOiJodHRwczovL3N0cy53aW5kb3dzLm5ldC8wYTE3NzEyYi02ZGYzLTQyNWQtODA4ZS0zMDlkZjI4YTVlZWIvIiwiaWF0IjoxNjgxODI5MDgzLCJuYmYiOjE2ODE4MjkwODMsImV4cCI6MTY4MTkxNTc4MywiYWNjdCI6MCwiYWNyIjoiMSIsImFpbyI6IkFUUUF5LzhUQUFBQTBVK2szWjFFbjl3bUxZdXVONDVNZHVhQ3J4d0Yvcmd4d3NxUjh5OHNLK1NxNnhwejd1aDZvSkVYdlU4cFBibTQiLCJhbXIiOlsicHdkIl0sImFwcF9kaXNwbGF5bmFtZSI6IkdyYXBoIEV4cGxvcmVyIiwiYXBwaWQiOiJkZThiYzhiNS1kOWY5LTQ4YjEtYThhZC1iNzQ4ZGE3MjUwNjQiLCJhcHBpZGFjciI6IjAiLCJmYW1pbHlfbmFtZSI6IkdpYWNjYWdsaWEiLCJnaXZlbl9uYW1lIjoiUGFibG8iLCJpZHR5cCI6InVzZXIiLCJpcGFkZHIiOiIxMzEuMTc1LjE0Ny4yOSIsIm5hbWUiOiJQYWJsbyBHaWFjY2FnbGlhIiwib2lkIjoiMzJiYjhlNjgtMGIxNy00YTgzLWFjZDctMDZkYjYwMTVkOGEwIiwib25wcmVtX3NpZCI6IlMtMS01LTIxLTY5NzM1OTY3OS0zOTU1MzgwMy0yNDE4ODY0MTYyLTQyODUzNiIsInBsYXRmIjoiNSIsInB1aWQiOiIxMDAzQkZGREExOTczNjUxIiwicmgiOiIwLkFUd0FLM0VYQ3ZOdFhVS0FqakNkOG9wZTZ3TUFBQUFBQUFBQXdBQUFBQUFBQUFBOEFOQS4iLCJzY3AiOiJGaWxlcy5SZWFkIEZpbGVzLlJlYWQuQWxsIEZpbGVzLlJlYWRXcml0ZS5BbGwgb3BlbmlkIHByb2ZpbGUgVXNlci5SZWFkIGVtYWlsIiwic2lnbmluX3N0YXRlIjpbImlua25vd25udHdrIiwia21zaSJdLCJzdWIiOiJaSzdnMFBtYlJJdkdDM1F5TGIzQ1EtUjB1cUlTU3NPMm1RVjF3WUplSzVnIiwidGVuYW50X3JlZ2lvbl9zY29wZSI6IkVVIiwidGlkIjoiMGExNzcxMmItNmRmMy00MjVkLTgwOGUtMzA5ZGYyOGE1ZWViIiwidW5pcXVlX25hbWUiOiIxMDYyNjQyOEBwb2xpbWkuaXQiLCJ1cG4iOiIxMDYyNjQyOEBwb2xpbWkuaXQiLCJ1dGkiOiJranBiWjZTMXdVT0RBSmdfUFlrS0FBIiwidmVyIjoiMS4wIiwid2lkcyI6WyJiNzlmYmY0ZC0zZWY5LTQ2ODktODE0My03NmIxOTRlODU1MDkiXSwieG1zX2NjIjpbIkNQMSJdLCJ4bXNfc3NtIjoiMSIsInhtc19zdCI6eyJzdWIiOiJVbjdHMV9qVElDRjQwOHBud3RKWmsyUFZRc0N1Um5iWW5PdklTYnlwMVRnIn0sInhtc190Y2R0IjoxMzI1Nzg0MDU2LCJ4bXNfdGRiciI6IkVVIn0.OKtDaHDT85X-7KQce_c2MHHr9Az-hUsw9S3iiwGz3DEW1Vd8dVsIVpTZWh4lCbzVmd6fustrjM5Zv6gC5F-m8AQIWeR1Mp_MCtGxmMWDDW_gxsELqRBM3jQtNA_TPEKn15NpDqxEl8bg3wdLLozPRt1v5t6CA7n5TiF46iorRvmRRHjlrKQra5fzMSY6uf7vmexc1TelMCRlKdPfhkWg0BnERQx_wfLHXWk3qr7AweEO0-Je8uMlo_mQgQ7ncNcvI_A-NAexD1xcNoR-BEPEwaOXoCSqalKFHsbnFfHurCB6v56UTLE9rVyYGp0B6vDS4UCdFgA58eziYaNCclsZOw"

    data_dict = utils.get_loaded_json_file(path = kaggle_images_json_dict)

    chunk1 = sorted(list(data_dict.keys()))[:50000]

    # SLICE 1

    start_time = time.time()

    cpu_count = mp.cpu_count()
    print(cpu_count)
    params = zip(chunk1,
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
