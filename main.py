# importing libraries and packages
from datetime import datetime
import utils

# 93 mins for 200k approx
if __name__ == '__main__':
    UNT_dataset_filename = "UNT_dataset/HurricaneHarvey_ids.txt"
    UNT_tweets_ids = utils.txt_to_list(filename = UNT_dataset_filename)

     #5761589 tweets needed
    # UNT_tweets_ids.index("903700320081113088")

    print(f"Number of UNT dataset tweets: {len(UNT_tweets_ids)}")
    print("UNT dataset building...")

    ranges = [1000000, 2000000, 3000000, 4000000, 5761589]
    start = 0
    for i in range(0, len(ranges)):
        print(f"Current ranges ({start} - {ranges[i]-1})")
        tweets =  UNT_tweets_ids[start: ranges[i]]
        utils.build_tweets_csv(tweets_ids = tweets, csv_filename = f"UNT_dataset_ids_{str(ranges[i])}.csv")
        start = ranges[i]


    print("UNT dataset building completed")

    Kaggle_dataset_filename = "Kaggle_dataset/TS_Harvey_Tweets.csv"
    start_date = datetime.strptime('2017-08-10', '%Y-%m-%d')
    end_date = datetime.strptime('2017-08-31', '%Y-%m-%d')
    Kaggle_tweets_ids = utils.get_tweets_ids_from_kaggle_dataset(Kaggle_dataset_filename = Kaggle_dataset_filename,
                                                                 start_date = start_date,
                                                                 end_date = end_date)

    print(f"Number of Kaggle dataset tweets: {len(Kaggle_tweets_ids)}")
    print("Kaggle dataset building...")
    utils.build_tweets_csv(tweets_ids = Kaggle_tweets_ids, csv_filename = "datasets_csv/Kaggle_dataset.csv") # 1059 seconds
    print("Kaggle dataset building complete")

    CrisisMMD_dataset_filename = "CrisisMMD_v2.0/json/hurricane_harvey_final_data.json"
    CrisisMMD_tweets_ids = utils.get_tweets_ids_from_crisismmd_dataset(
            CrisisMMD_datset_filename = CrisisMMD_dataset_filename,
            start_date = start_date,
            end_date = end_date)
    "cp usr/uplink-c/libuplinkc.so /opt/conda/lib/python3.10/site-packages/uplink_python"
    print(f"Number of CrisisMMD dataset tweets: {len(CrisisMMD_tweets_ids)}")
    print("CrisisMMD dataset building...")
    utils.build_tweets_csv(tweets_ids = CrisisMMD_tweets_ids, csv_filename = "datasets_csv/CrisisMMD_dataset.csv") # 12 seconds
    print("CrisisMMD dataset building completed")

    ids = list(set(UNT_tweets_ids + Kaggle_tweets_ids + CrisisMMD_tweets_ids))
    num_duplicates = len(UNT_tweets_ids + Kaggle_tweets_ids + CrisisMMD_tweets_ids) - len(ids)

    print(f"Number of duplicate tweets among datasets: {num_duplicates}")
