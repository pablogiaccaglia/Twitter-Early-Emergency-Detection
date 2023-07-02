# 🐦 Twitter-Early-Emergency-Detection

- 📙 [Description](#-description)
- 📦 [Repo content](#-repo-content)
- ⚙️ [Pipeline](#-Pipeline)
- 💾 [Explored Inputs](#-explored-inputs)
- 🧠 [Models Explored](#-models-explored)
- 📋 [Performance Results](#-performance-results)
- 📜 [Generated picture captions](#-generated-picture-captions)


# 📙 Description
Early Detection and Rapid Response (**EDRR**) to natural disasters is a laborious task. It is important to have rapid detection for early response.
Tweets can provide a low-latency source of first-hand information. There are numerous possibilities to make use of them for improval of situation, such as the detection of
a catastrophe's outbreak, follow the situation without being on-site and locate hotspots, even without geo-data.

# 📦 Repo content
- [tweets_scrape.py](https://github.com/pablogiaccaglia/Twitter-Early-Emergency-Detection/blob/master/tweets_scrape.py) -> script for scraping the tweets of the various dataset reported below
- [CRISISMMD_IMAGES](https://github.com/pablogiaccaglia/Twitter-Early-Emergency-Detection/tree/master/CRISISMMD_IMAGES):
  - [CrisisMMD](https://crisisnlp.qcri.org/crisismmd) **3357 images** scraped from the web through script contained [here](https://github.com/pablogiaccaglia/Twitter-Early-Emergency-Detection/tree/master/CrisisMMD_v2.0)
- [CrisisMMD_v2.0](https://github.com/pablogiaccaglia/Twitter-Early-Emergency-Detection/tree/master/CrisisMMD_v2.0)
  - The folder contains scripts and files relevant to the [CrisisMMD](https://crisisnlp.qcri.org/crisismmd) dataset. Here the most important ones:
    - [crisismd_images_scrape.py](https://github.com/pablogiaccaglia/Twitter-Early-Emergency-Detection/blob/master/CrisisMMD_v2.0/crisismd_images_scrape.py)
    - [crisismmd_BILP2-generated-sentences.json](https://github.com/pablogiaccaglia/Twitter-Early-Emergency-Detection/blob/master/CrisisMMD_v2.0/crisismmd_BILP2-generated-sentences.json) -> json dict containing generated captions ( **key: image file name , value: caption**)
    - [crisismmd_sintetic_tweets.py](https://github.com/pablogiaccaglia/Twitter-Early-Emergency-Detection/blob/master/CrisisMMD_v2.0/crisismmd_sintetic_tweets.py) -> script for generating synthetic tweets through **ChatGPT**
    - [/CrisisMMD_final_dataset_captions_with_stweets.csv](https://github.com/pablogiaccaglia/Twitter-Early-Emergency-Detection/blob/master/CrisisMMD_v2.0/CrisisMMD_final_dataset_captions_with_stweets.csv) -> final csv with **generated captions** and **synthetic tweets**, without labels (these are contained [here](https://github.com/pablogiaccaglia/Twitter-Early-Emergency-Detection/blob/master/CrisisMMD_v2.0/json/hurricane_harvey_final_data.json))
- [EDA+experiments.ipynb](https://github.com/pablogiaccaglia/Twitter-Early-Emergency-Detection/blob/master/EDA%2Bexperiments.ipynb)
  - This notebook comprises preliminary exploratory data analysis and all the experiments for achieving the results shown below.
 [crisis-tweets-data](https://github.com/pablogiaccaglia/Twitter-Early-Emergency-Detection/tree/master/tweets-data)
  - This folder contains the most relevant files related to** CrisisMMD dataset**, which are:
    - [CrisisMMD_final_dataset_captions_with_stweets.csv] -> final csv with **generated captions** and **synthetic tweets**, without labels (these are contained [here](https://github.com/pablogiaccaglia/Twitter-Early-Emergency-Detection/blob/master/tweets-data/hurricane_harvey_final_data.xlsx))
    - [crisismd_tweets_media_urls.json]() -> json dict containing urls of the scraped images
(**key: tweet text content, value: list of urls**)
    - [crisismmd_BILP2-generated-sentences.json](https://github.com/pablogiaccaglia/Twitter-Early-Emergency-Detection/blob/master/CrisisMMD_v2.0/crisismmd_BILP2-generated-sentences.json) -> json dict containing generated captions 
( **key: image file name , value: caption**)
    - [hurricane_harvey_final_data.xlsx](https://github.com/pablogiaccaglia/Twitter-Early-Emergency-Detection/blob/master/tweets-data/hurricane_harvey_final_data.xlsx) -> contains the labels associated with the crisismmd tweets

- Additional datasets used for experimenting different approaches (not contained in this repository). The folders contains both scraping & generation scripts and structured resulting data
  
  - [Kaggle_dataset](https://github.com/pablogiaccaglia/Twitter-Early-Emergency-Detection/tree/master/Kaggle_dataset) -> [source](https://www.kaggle.com/datasets/dan195/hurricaneharvey)
  - [UNT_dataset](https://github.com/pablogiaccaglia/Twitter-Early-Emergency-Detection/tree/master/UNT_dataset) -> [source](https://digital.library.unt.edu/ark:/67531/metadc993940/#collections)

- [additional-labelled-tweets](https://github.com/pablogiaccaglia/Twitter-Early-Emergency-Detection/tree/master/additional-labelled-tweets) -> additional manually labeled tweets by us coming from the UNT dataset
# ⚙️ Pipeline
![alt text](https://github.com/pablogiaccaglia/Twitter-Early-Emergency-Detection/blob/master/media/pipeline.svg)

Here we have an overview of the implemented pipeline. 
The main component is the **Tweet Classifier** which can be a **Bert** or a **Glove-based** model, which outputs a relevancy score with respect to a **“Humanitarian Aid” definition**. 
The peculiarity of this model is that it leverages several textual inputs that we have explored in different combinations, 
starting from tweets that always contain text and eventually images. 
Labeled tweets, produced with different approaches, have been used for generating additional inputs, such as AI-generated tweets. 
All this textual information has been pre-processed through classical routines, such as mentions removal and url removal.

# 💾 Explored Inputs
![alt text](https://github.com/pablogiaccaglia/Twitter-Early-Emergency-Detection/blob/master/media/explored-inputs.svg)
To train the tweet classification model, we leverage various sources of information. Here some infos:
- **Expert-labelled Tweets**: A collection of tweets manually labeled by domain experts as either relevant or irrelevant to the disaster
  - **CrisisMMD Dataset**: Strictly related to Hurricane Harvey
  - 3991 Tweets
  - Tweet is relevant if useful for **“Humanitarian aid”**
  - Available [here](https://github.com/pablogiaccaglia/Twitter-Early-Emergency-Detection/blob/master/tweets-data/hurricane_harvey_final_data.xlsx)
- **AI-generated Picture Captions**: Automatically generated captions for disaster-related images using computer vision techniques
  - Captions of Tweets’ images
  - Done with [**BILP Vision-LLM**](https://github.com/salesforce/BLIP)
  - High-quality descriptions
  - Expensive model: **80GB of RAM required for inference**
  - Available [here](https://github.com/pablogiaccaglia/Twitter-Early-Emergency-Detection/blob/master/CrisisMMD_v2.0/crisismmd_BILP2-generated-sentences.json)

- **Manually-labelled Tweets**: Additional tweets labeled by us to expand the training dataset
  - Double-agreement labels
  - Not always easy to get the “humanitarian aid” definition
  - **Distribution shift** w.r.t CrisisMMD worsened model performance
  - Available [here](https://github.com/pablogiaccaglia/Twitter-Early-Emergency-Detection/tree/master/additional-labelled-tweets)

- **Pseudo-labelled Tweets**: Tweets labeled based on predictions made by the model itself, augmenting the training data
  - Aimed to enlarge training set
  - Didn’t solve the class imbalance
  - **A lot of false positives**
  - Worsened model performance

- **AI-generated Tweets for Training**: Tweets generated using ChatGPT
  - ChatGPT-based generation 
  - Data augmentation of training set
  - Didn’t solve the class imbalance
  - Worsened model performance
  - Available [here](https://github.com/pablogiaccaglia/Twitter-Early-Emergency-Detection/blob/master/CrisisMMD_v2.0/json/hurricane_harvey_final_data.json)

# 🧠 Models Explored
To classify the disaster-related tweets, we explore the following models:

- Bert-based Models
  - **Bert (base uncased)** based classifier: A classifier based on the Bert architecture, a state-of-the-art transformer-based model for natural language processing tasks.
  - **roBERTa (disaster tweets fine-tuned)** based classifier: A variant of the **Bert model** specifically fine-tuned on disaster-related tweets for improved performance.
-  High performance & computational requirements: These models offer higher accuracy but require more computational resources for training and inference.

- Glove-based Models
  - **Glove (27B Twitter)** based classifier: A classifier based on the **Glove embedding model** trained on a large corpus of Twitter data.
  - Better for fast and inexpensive training & inference: These models provide a balance between accuracy and computational efficiency, making them suitable for fast training and inference on resource-constrained systems.

# 📋 Performance Results
The table below presents the performance results of the various models in terms of precision, recall, and accuracy
![alt text](https://github.com/pablogiaccaglia/Twitter-Early-Emergency-Detection/blob/master/media/performance.svg)

# 📜 Generated picture captions
![alt text](https://github.com/pablogiaccaglia/Twitter-Early-Emergency-Detection/blob/master/media/ai-captions.svg)

The introduction of picture caption helped the model in achieving a better overall performance. 
This is likely due to the fact that these descriptions provide additional information about the semantics of the tweet, 
allowing for less uncertain predictions, especially for the cases in which the description of the image content 
highly determines the predicted label.

![alt text](https://github.com/pablogiaccaglia/Twitter-Early-Emergency-Detection/blob/master/media/image-caption.svg)





