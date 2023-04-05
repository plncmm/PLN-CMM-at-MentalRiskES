from data import gen_data, split_train_test, make_dict
from model import FeedforwardNeuralNetModel
from train import train
from evaluate import evaluate
import torch.optim as optim
import torch.nn as nn
import torch
import os
import matplotlib.pyplot as plt

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print("Device available for running: ")
print(device)

if __name__ == "__main__":
    output_folder = '../../../logs/'
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        

    task = "task1"
    x = list(range(5))
    y = []
    for i in range(5):

        log_filename = f"{output_folder}ffnn_bow_round_{i}.csv"
        df = gen_data(task, i+1)
        X_train, X_test, Y_train, Y_test = split_train_test(df)
        review_dict = make_dict(df, padding=True)
        vocab_size = len(review_dict)
        input_dim = vocab_size
        hidden_dim = 500
        output_dim = 2
        num_epochs = 100

        ff_nn_bow_model = FeedforwardNeuralNetModel(input_dim, hidden_dim, output_dim)
        ff_nn_bow_model.to(device)

        loss_function = nn.CrossEntropyLoss()
        optimizer = optim.SGD(ff_nn_bow_model.parameters(), lr=0.01)

        train(
            ff_nn_bow_model,
            X_train,
            Y_train,
            review_dict,
            vocab_size,
            optimizer,
            loss_function,
            num_epochs,
            device,
            log_filename,
        )

        f1 = evaluate(
            ff_nn_bow_model, X_test, Y_test, review_dict, vocab_size, device, log_filename
        )

        y.append(f1)
    print(x)
    print(y)
    plt.plot(x, y)
    plt.title('F1-score against comment rounds')
    plt.xlabel('Round')
    plt.ylabel('F1 Score')
    plt.show()



