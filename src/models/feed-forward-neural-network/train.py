import numpy as np
from tqdm import tqdm
from data import make_bow_vector, make_target


def train(
    model,
    texts,
    targets,
    review_dict,
    vocab_size,
    optimizer,
    loss_function,
    epochs,
    device,
    log_file
):
    ffnn_loss_file_name = log_file
    f = open(ffnn_loss_file_name, "w")
    f.write("iter, loss")
    f.write("\n")
    losses = []
    iter = 0
    min_valid_loss = np.inf
    bad_epochs = 0
    # Start training
    for epoch in tqdm(range(epochs), total=epochs, desc='Training FFNN model..'):
        train_loss = 0
        model.train()
        for index, row in texts.iterrows():
            # Clearing the accumulated gradients
            optimizer.zero_grad()

            # Make the bag of words vector for stemmed tokens
            # bow_vec = make_bow_vector(review_dict, row['tokenized_text'])

            bow_vec = make_bow_vector(
                review_dict, row["tokenized_text"], vocab_size, device
            )

            # Forward pass to get output
            probs = model(bow_vec)

            # Get the target label
            target = make_target(targets["label"][index], device)

            # Calculate Loss: softmax --> cross entropy loss
            loss = loss_function(probs, target)
            # Accumulating the loss over time
            train_loss += loss.item()

            # Getting gradients w.r.t. parameters
            loss.backward()

            # Updating parameters
            optimizer.step()

        f.write(str((epoch + 1)) + "," + str(train_loss / len(texts)))
        f.write("\n")
        train_loss = 0
