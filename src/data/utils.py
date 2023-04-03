import requests, zipfile, io, os 
from typing import List, Dict

URL = "http://s3-ceatic.ujaen.es:8036/" 
TOKEN = "789c16fe57f3bc7f0108525b1ea89a0bb4a4952b" 

# Download endpoints
ENDPOINT_DOWNLOAD_MESSAGES_TRIAL = URL+"{TASK}/download_trial/{TOKEN}"
ENDPOINT_DOWNLOAD_GOLD_TRIAL = URL+"{SUBTASK}/download_trial/{TOKEN}"
ENDPOINT_DOWNLOAD_MESSAGES_TRAIN = URL+"{TASK}/download_train/{TOKEN}"
ENDPOINT_DOWNLOAD_GOLD_TRAIN = URL+"{SUBTASK}/download_train/{TOKEN}"

# Trial endpoints
ENDPOINT_GET_MESSAGES_TRIAL = URL+"{TASK}/getmessages_trial/{TOKEN}"
ENDPOINT_SUBMIT_DECISIONS_TRIAL = URL+"{SUBTASK}/submit_trial/{TOKEN}/{RUN}"

# Test endpoints
ENDPOINT_GET_MESSAGES = URL+"{TASK}/getmessages/{TOKEN}"
ENDPOINT_SUBMIT_DECISIONS = URL+"{SUBTASK}/submit/{TOKEN}/{RUN}"

def download_messages_train(task: str,subtasks:List[str], token: str) -> List[Dict]:
    response = requests.get(ENDPOINT_DOWNLOAD_MESSAGES_TRAIN.format(TASK=task, TOKEN=token))

    if response.status_code != 200:
        print("Train - Status Code " + task + ": " + str(response.status_code) + " - Error: " + str(response.text))
    else:
      z = zipfile.ZipFile(io.BytesIO(response.content))
      os.makedirs("../../data/raw/{task}/train/subjects_train/".format(task=task))
      z.extractall("../../data/raw/{task}/train/subjects_train/".format(task=task))

    for subtask in subtasks:
        response = requests.get(ENDPOINT_DOWNLOAD_GOLD_TRAIN.format(SUBTASK=subtask, TOKEN=token))
        
        if response.status_code != 200:
            print("Train - Status Code " + subtask + ": " + str(response.status_code) + " - Error: " + str(response.text))
        else:
          file_object = open("../../data/raw/{task}/train/gold_train_{subtask}.txt".format(task=task, subtask=subtask), "w")
          file_object.write(response.text)

def download_data(task):
    if task==1:
        download_messages_train("task1", ["task1a", "task1b"], TOKEN)
    if task==2:
        download_messages_train("task2", ["task2a", "task2b", "task2c", "task2d"], TOKEN)
    if task==3:
        download_messages_train("task3", ["task3a", "task3b"], TOKEN)
    
