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

    crisismd_images_json_dict = "CrisisMMD_v2.0/crisismd_tweets_media_urls.json"
    ONEDRIVE_FOLDER_ID = "01NU2AK4X32EG42CDKHVH2UFPK576I6PR6"
    AT = "eyJ0eXAiOiJKV1QiLCJub25jZSI6IjZuN2VqZWNYSXF0MzEzeHZRbS1OM3lvMkh6TVVSU1ViUjdEbzFDWmVNbkEiLCJhbGciOiJSUzI1NiIsIng1dCI6Ii1LSTNROW5OUjdiUm9meG1lWm9YcWJIWkdldyIsImtpZCI6Ii1LSTNROW5OUjdiUm9meG1lWm9YcWJIWkdldyJ9.eyJhdWQiOiIwMDAwMDAwMy0wMDAwLTAwMDAtYzAwMC0wMDAwMDAwMDAwMDAiLCJpc3MiOiJodHRwczovL3N0cy53aW5kb3dzLm5ldC8wYTE3NzEyYi02ZGYzLTQyNWQtODA4ZS0zMDlkZjI4YTVlZWIvIiwiaWF0IjoxNjgwODYyMjc0LCJuYmYiOjE2ODA4NjIyNzQsImV4cCI6MTY4MDk0ODk3NCwiYWNjdCI6MCwiYWNyIjoiMSIsImFpbyI6IkFUUUF5LzhUQUFBQVEwenp3aGk5MDhCblozd2hteE9Damc0bnMvRDlxQTh3RFhuVU5qYVhRT3Z4UjdaRm5Fa29SSzF2WDd4cnZQbzIiLCJhbXIiOlsicHdkIl0sImFwcF9kaXNwbGF5bmFtZSI6IkdyYXBoIEV4cGxvcmVyIiwiYXBwaWQiOiJkZThiYzhiNS1kOWY5LTQ4YjEtYThhZC1iNzQ4ZGE3MjUwNjQiLCJhcHBpZGFjciI6IjAiLCJmYW1pbHlfbmFtZSI6IkdpYWNjYWdsaWEiLCJnaXZlbl9uYW1lIjoiUGFibG8iLCJpZHR5cCI6InVzZXIiLCJpcGFkZHIiOiIxNzYuMjA3LjI2LjEyMiIsIm5hbWUiOiJQYWJsbyBHaWFjY2FnbGlhIiwib2lkIjoiMzJiYjhlNjgtMGIxNy00YTgzLWFjZDctMDZkYjYwMTVkOGEwIiwib25wcmVtX3NpZCI6IlMtMS01LTIxLTY5NzM1OTY3OS0zOTU1MzgwMy0yNDE4ODY0MTYyLTQyODUzNiIsInBsYXRmIjoiNSIsInB1aWQiOiIxMDAzQkZGREExOTczNjUxIiwicmgiOiIwLkFUd0FLM0VYQ3ZOdFhVS0FqakNkOG9wZTZ3TUFBQUFBQUFBQXdBQUFBQUFBQUFBOEFOQS4iLCJzY3AiOiJGaWxlcy5SZWFkIEZpbGVzLlJlYWQuQWxsIEZpbGVzLlJlYWRXcml0ZS5BbGwgb3BlbmlkIHByb2ZpbGUgVXNlci5SZWFkIGVtYWlsIiwic3ViIjoiWks3ZzBQbWJSSXZHQzNReUxiM0NRLVIwdXFJU1NzTzJtUVYxd1lKZUs1ZyIsInRlbmFudF9yZWdpb25fc2NvcGUiOiJFVSIsInRpZCI6IjBhMTc3MTJiLTZkZjMtNDI1ZC04MDhlLTMwOWRmMjhhNWVlYiIsInVuaXF1ZV9uYW1lIjoiMTA2MjY0MjhAcG9saW1pLml0IiwidXBuIjoiMTA2MjY0MjhAcG9saW1pLml0IiwidXRpIjoibndONi1FcVY1MDJlYVI2c1U5STZBQSIsInZlciI6IjEuMCIsIndpZHMiOlsiYjc5ZmJmNGQtM2VmOS00Njg5LTgxNDMtNzZiMTk0ZTg1NTA5Il0sInhtc19jYyI6WyJDUDEiXSwieG1zX3NzbSI6IjEiLCJ4bXNfc3QiOnsic3ViIjoiVW43RzFfalRJQ0Y0MDhwbnd0SlprMlBWUXNDdVJuYlluT3ZJU2J5cDFUZyJ9LCJ4bXNfdGNkdCI6MTMyNTc4NDA1NiwieG1zX3RkYnIiOiJFVSJ9.N6kci4kl1Yr-bdgboB2fcrc4mMK3Tgyu-J1-7Ygvo-HzAgFWetMSuhmpN_-XaTFu-Z4D1uHqF02nSxbrkT6CbTq9D_OV5un7SsrDKWGpPZoEU3xXmvgOk2fjg8v70af9kApSEacASczO4p3I52O1syBk8t-Mo0MmEHYcbzC5HMpgfxQug8Inr1aVrkx8ck_hQ2bunWExA9aD0fT1f9zRTEnKzQImJkX6u4VE9d948sqc2xvToWFhOEGYjzl48YuJa1Txe38vQt-7xTjqzBEdKjWyH48ofxZc2GZwL-Umxo8KSK3vSKXBL09sa00GGDFSt6a1o3n9CIuuAdaQd5nKwQ"
    data_dict = utils.get_loaded_json_file(path = crisismd_images_json_dict)

    start_time = time.time()

    cpu_count = mp.cpu_count()
    print(cpu_count)
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
