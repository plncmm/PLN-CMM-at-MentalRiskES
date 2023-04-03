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
        
def get_annotations(path):
    d = {}
    content = open(path,'r').read()
    for line in content.splitlines()[1:]:
        filename, label = line.split(',')
        d[filename]=label
    return d

def get_paths(directory_path):
    return [path for path in glob.glob(f'{directory_path}/*.json')]
    
if __name__=='__main__':
    train_annotations_2a = get_annotations('task2/train/gold_train_task2a.txt')
    train_annotations_2b = get_annotations('task2/train/gold_train_task2b.txt')
    train_text_paths = get_paths('task2/train/subjects_train')
    train_texts = get_texts_from_json_files(train_text_paths)
    format_data_task(train_texts, train_annotations_2b, 'data2b.csv')
