# importing libraries and packages
from datetime import datetime
import utils

if __name__ == '__main__':
    UNT_dataset_filename = "UNT_dataset/HurricaneHarvey_ids.txt"
    UNT_tweets_ids = utils.txt_to_list(filename = UNT_dataset_filename)[200000:400000]
    utils.build_tweets_csv(tweets_ids = UNT_tweets_ids, csv_filename = "UNT_dataset_200k_400k.csv")

    Kaggle_dataset_filename = "Kaggle_dataset/TS_Harvey_Tweets.csv"
    start_date = datetime.strptime('2017-08-10', '%Y-%m-%d')
    end_date = datetime.strptime('2017-08-31', '%Y-%m-%d')
    Kaggle_tweets_ids = utils.get_tweets_ids_from_kaggle_dataset(Kaggle_dataset_filename = Kaggle_dataset_filename,
                                                                 start_date = start_date,
                                                                 end_date = end_date)

    CrisisMMD_dataset_filename = "CrisisMMD_v2.0/json/hurricane_harvey_final_data.json"
    CrisisMMD_tweets_ids = utils.get_tweets_ids_from_crisismmd_dataset(
            CrisisMMD_datset_filename = CrisisMMD_dataset_filename,
            start_date = start_date,
            end_date = end_date)

    print(f"Number of UNT dataset tweets: {len(UNT_tweets_ids)}")
    print(f"Number of Kaggle dataset tweets: {len(Kaggle_tweets_ids)}")
    print(f"Number of CrisisMMD dataset tweets: {len(CrisisMMD_tweets_ids)}")

    ids = list(set(UNT_tweets_ids + Kaggle_tweets_ids + CrisisMMD_tweets_ids))
    num_duplicates = len(UNT_tweets_ids + Kaggle_tweets_ids + CrisisMMD_tweets_ids) - len(ids)

    print(f"Number of duplicate tweets among datasets: {num_duplicates}")
