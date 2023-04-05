from sklearn.metrics import f1_score
from sklearn.metrics import classification_report
from data import make_bow_vector, make_target
import torch
import pandas as pd

# Calculating the MAE with a custom function
import numpy as np


def mae(y_true, predictions):
    y_true, predictions = np.array(y_true), np.array(predictions)
    return np.mean(np.abs(y_true - predictions))


def evaluate(model, X_test, Y_test, review_dict, vocab_size, device, log_filename):
    real = []
    preds = []

    with torch.no_grad():
        for index, row in X_test.iterrows():
            bow_vec = make_bow_vector(
                review_dict, row["tokenized_text"], vocab_size, device
            )
            probs = model(bow_vec)
            preds.append(torch.argmax(probs, dim=1).cpu().numpy()[0])
            real.append(make_target(Y_test["label"][index], device).cpu().numpy()[0])
    print(classification_report(real, preds))
    #ffnn_loss_df = pd.read_csv(log_filename)
    #ffnn_plt_500_padding_100_epochs = ffnn_loss_df[" loss"].plot()
    #fig = ffnn_plt_500_padding_100_epochs.get_figure()
    #fig.savefig("plots_ffnn_bow_loss_500_padding_100_epochs_less_lr.pdf")
    return round(f1_score(real, preds), 2)
