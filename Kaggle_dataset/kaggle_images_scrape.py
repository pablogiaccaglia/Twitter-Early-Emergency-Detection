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

    kaggle_images_json_dict = "kaggle_tweets_media_urls.json"
    ONEDRIVE_FOLDER_ID = "01NU2AK4XP4CQJOQLM2NHIFXAFHFLMPAMH"
    AT = "eyJ0eXAiOiJKV1QiLCJub25jZSI6IlY3WVdHMzJPNmZrekU0VkZuLUtnZ0EyT2FFcU9Pd2syUWlmQXVYYXdwa28iLCJhbGciOiJSUzI1NiIsIng1dCI6Ii1LSTNROW5OUjdiUm9meG1lWm9YcWJIWkdldyIsImtpZCI6Ii1LSTNROW5OUjdiUm9meG1lWm9YcWJIWkdldyJ9.eyJhdWQiOiIwMDAwMDAwMy0wMDAwLTAwMDAtYzAwMC0wMDAwMDAwMDAwMDAiLCJpc3MiOiJodHRwczovL3N0cy53aW5kb3dzLm5ldC8wYTE3NzEyYi02ZGYzLTQyNWQtODA4ZS0zMDlkZjI4YTVlZWIvIiwiaWF0IjoxNjgxNzMwMzAwLCJuYmYiOjE2ODE3MzAzMDAsImV4cCI6MTY4MTgxNzAwMCwiYWNjdCI6MCwiYWNyIjoiMSIsImFpbyI6IkFUUUF5LzhUQUFBQWNiZ3BFbEdRRGUrbXRyVUxzRE5HQjYrcTVScnBFQWplZTV3VnpOcVhjL2ZBUHY4b0VTdVBoanZEQzZZcUFQMzciLCJhbXIiOlsicHdkIl0sImFwcF9kaXNwbGF5bmFtZSI6IkdyYXBoIEV4cGxvcmVyIiwiYXBwaWQiOiJkZThiYzhiNS1kOWY5LTQ4YjEtYThhZC1iNzQ4ZGE3MjUwNjQiLCJhcHBpZGFjciI6IjAiLCJmYW1pbHlfbmFtZSI6IkdpYWNjYWdsaWEiLCJnaXZlbl9uYW1lIjoiUGFibG8iLCJpZHR5cCI6InVzZXIiLCJpcGFkZHIiOiIxMzEuMTc1LjE0Ny4zIiwibmFtZSI6IlBhYmxvIEdpYWNjYWdsaWEiLCJvaWQiOiIzMmJiOGU2OC0wYjE3LTRhODMtYWNkNy0wNmRiNjAxNWQ4YTAiLCJvbnByZW1fc2lkIjoiUy0xLTUtMjEtNjk3MzU5Njc5LTM5NTUzODAzLTI0MTg4NjQxNjItNDI4NTM2IiwicGxhdGYiOiI1IiwicHVpZCI6IjEwMDNCRkZEQTE5NzM2NTEiLCJyaCI6IjAuQVR3QUszRVhDdk50WFVLQWpqQ2Q4b3BlNndNQUFBQUFBQUFBd0FBQUFBQUFBQUE4QU5BLiIsInNjcCI6IkZpbGVzLlJlYWQgRmlsZXMuUmVhZC5BbGwgRmlsZXMuUmVhZFdyaXRlLkFsbCBvcGVuaWQgcHJvZmlsZSBVc2VyLlJlYWQgZW1haWwiLCJzaWduaW5fc3RhdGUiOlsiaW5rbm93bm50d2siLCJrbXNpIl0sInN1YiI6IlpLN2cwUG1iUkl2R0MzUXlMYjNDUS1SMHVxSVNTc08ybVFWMXdZSmVLNWciLCJ0ZW5hbnRfcmVnaW9uX3Njb3BlIjoiRVUiLCJ0aWQiOiIwYTE3NzEyYi02ZGYzLTQyNWQtODA4ZS0zMDlkZjI4YTVlZWIiLCJ1bmlxdWVfbmFtZSI6IjEwNjI2NDI4QHBvbGltaS5pdCIsInVwbiI6IjEwNjI2NDI4QHBvbGltaS5pdCIsInV0aSI6IklVLWlEQkFqcUVxamFCRGpsNzBkQUEiLCJ2ZXIiOiIxLjAiLCJ3aWRzIjpbImI3OWZiZjRkLTNlZjktNDY4OS04MTQzLTc2YjE5NGU4NTUwOSJdLCJ4bXNfY2MiOlsiQ1AxIl0sInhtc19zc20iOiIxIiwieG1zX3N0Ijp7InN1YiI6IlVuN0cxX2pUSUNGNDA4cG53dEpaazJQVlFzQ3VSbmJZbk92SVNieXAxVGcifSwieG1zX3RjZHQiOjEzMjU3ODQwNTYsInhtc190ZGJyIjoiRVUifQ.R9NWJzl271HPH4xxKsT5tmQ7THjNnm5dHRj1IrBlfwwFzwRypn5krZIyGiHpKHIepJKJ2qiHPNv36pwhhVxJUyLpXKTVwqmjwTYLwtr6qHM1y6Vd6fAG_sRGv8KJVNwylYqKMZKQEA1Q1KofQs21ffZRmyxb0ehPKFSyRwShOoM5J2I2msJtyRU7OerveFxG_U-S9ey4SAGTrJ4VXxrCtv-IG4-7fbN8G5J7kVp0ViUm0T0c_7l7Ayl7yQP_bsC9wfxcSbfQp5TwJCW9vtu-nrPVwO6oy6ZJSDuvRWvA-wn0aYUW5yifT8Wa60krx18yDXJe5NM6PLhFbEjF5qd8Bg"
    data_dict = utils.get_loaded_json_file(path = kaggle_images_json_dict)

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
