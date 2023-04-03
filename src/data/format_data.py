import glob
import json 
import os
import pandas as pd

def get_texts_from_json_files(paths):
    d = {}
    for path in paths:
        f = open(path)
        data = json.load(f)
        text = ''
        for message in data:
            text += message['message']
            text += ' '
        d[os.path.basename(path).split('.')[0]]=text
    return d

def format_data_task(text_dict, annotations, output_filename):
    d = {'filename': [], 'text':[], 'label':[]}
    for filename, text in text_dict.items():
        d["filename"].append(filename)
        d["text"].append(text)
        d["label"].append(annotations[filename])
    df = pd.DataFrame(d)
    df.to_csv(output_filename, index=False)
    

        
def get_annotations(path, subtask):
    if subtask!='task2d':
        d = {}
        content = open(path,'r').read()
        for line in content.splitlines()[1:]:
            filename, label = line.split(',')
            d[filename]=label
    else:
        d = {}
        content = open(path,'r').read()
        for line in content.splitlines()[1:]:
            filename = line.split(',')[0]
            labels = line.split(',')[1:]
            d[filename]=labels
    return d

def get_paths(directory_path):
    return [path for path in glob.glob(f'{directory_path}/*.json')]

def format_files(task):

    if task=='task1':
        subtasks = ['task1a', 'task1b']
        for st in subtasks:
            train_annotations= get_annotations(f'../../data/raw/{task}/train/gold_train_{st}.txt', st)
            train_text_paths = get_paths(f'../../data/raw/{task}/train/subjects_train')
            train_texts = get_texts_from_json_files(train_text_paths)
            format_data_task(train_texts, train_annotations, f'../../data/processed/data_{st}.csv')
    
    if task=='task2':
        subtasks = ['task2a', 'task2b', 'task2c', 'task2d']
        for st in subtasks:
            train_annotations= get_annotations(f'../../data/raw/{task}/train/gold_train_{st}.txt', st)
            train_text_paths = get_paths(f'../../data/raw/{task}/train/subjects_train')
            train_texts = get_texts_from_json_files(train_text_paths)
            format_data_task(train_texts, train_annotations, f'../../data/processed/data_{st}.csv')

if __name__=='__main__':
    format_files('task1')
    format_files('task2')