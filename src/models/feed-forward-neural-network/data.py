from pandas import DataFrame
from nltk.corpus import stopwords
from gensim.utils import simple_preprocess
from sklearn.model_selection import train_test_split
from gensim import corpora
import nltk
import pandas as pd
import string
import torch

nltk.download("stopwords")

stop = stopwords.words("spanish")
stop = list(stop)
stop.remove("mía")


def gen_data(task: str, n_messages: int) -> DataFrame:
    df_classification = pd.read_csv(
        f"../../../data/processed/data_{task}a_round_{n_messages}.csv", sep=","
    )
    df_regression = pd.read_csv(
        f"../../../data/processed/data_{task}b_round_{n_messages}.csv", sep=","
    )
    df = df_classification.merge(df_regression, on=["filename", "text"])
    df = df.rename(columns={"filename": "id", "label_x": "label", "label_y": "prob"})
    df["text"] = df["text"].apply(preprocessing)
    df = tokenize(df)
    return df


def preprocessing(
    text: str,
    to_lower: bool = True,
    remove_punctuations: bool = True,
    remove_stop_words: bool = True,
) -> str:
    if to_lower:
        text = text.lower()
    if remove_punctuations:
        for char in string.punctuation:
            text = text.replace(char, "")
    if remove_stop_words:
        text = " ".join(
            [word for word in text.split() if word not in list(stop) + ["q"]]
        )
    return text


def tokenize(df: DataFrame) -> DataFrame:
    df["tokenized_text"] = [simple_preprocess(line, deacc=True) for line in df["text"]]
    return df


def split_train_test(df, test_size=0.3, shuffle_state=True):
    X_train, X_test, Y_train, Y_test = train_test_split(
        df[["id", "text", "tokenized_text", "prob"]],
        df["label"],
        shuffle=shuffle_state,
        test_size=test_size,
        random_state=15,
    )

    X_train = X_train.reset_index()
    X_test = X_test.reset_index()
    Y_train = Y_train.to_frame()
    Y_train = Y_train.reset_index()
    Y_test = Y_test.to_frame()
    Y_test = Y_test.reset_index()
    return X_train, X_test, Y_train, Y_test


def make_dict(df, padding=True):
    if padding:
        print("Dictionary with padded token added")
        review_dict = corpora.Dictionary([["pad"]])
        review_dict.add_documents(df["tokenized_text"])
    else:
        print("Dictionary without padding")
        review_dict = corpora.Dictionary(df["tokenized_text"])
    return review_dict


def make_bow_vector(review_dict, sentence, vocab_size, device):
    vec = torch.zeros(vocab_size, dtype=torch.float64, device=device)
    for word in sentence:
        vec[review_dict.token2id[word]] += 1
    return vec.view(1, -1).float()


def make_target(label, device):
    if label == 0:
        return torch.tensor([0], dtype=torch.long, device=device)
    else:
        return torch.tensor([1], dtype=torch.long, device=device)


if __name__ == "__main__":
    df = gen_data("task2", 1)
    df = tokenize(df)
    print(df.head())
