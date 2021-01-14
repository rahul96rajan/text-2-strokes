import math
import os
import argparse
import time
import numpy as np
import matplotlib.pyplot as plt
import torch
import torch.nn as nn
import torch.optim as optim
from torch.optim.lr_scheduler import StepLR
from torch.utils.data import DataLoader
from models.models import HandWritingPredictionNet, HandWritingSynthesisNet
from generate import generate_conditional_sequence, generate_unconditional_seq
from utils.data_utils import data_denormalization
from utils.model_utils import compute_nll_loss
from utils.dataset import HandwritingDataset
from utils.constants import Global
from utils import plot_stroke
# from torch.utils import data
# from torch.distributions import bernoulli, uniform
# import torch.nn.functional as F
# import matplotlib
# matplotlib.use("Agg")


def argparser():

    parser = argparse.ArgumentParser(
        description="PyTorch Handwriting Synthesis Model")
    parser.add_argument("--hidden_size", type=int, default=400)
    parser.add_argument("--n_layers", type=int, default=3)
    parser.add_argument("--batch_size", type=int, default=32)
    parser.add_argument("--step_size", type=int, default=100)
    parser.add_argument("--n_epochs", type=int, default=100)
    parser.add_argument("--lr", type=float, default=0.001)
    parser.add_argument("--patience", type=int, default=15)
    parser.add_argument("--model_type", type=str, default="prediction")
    parser.add_argument("--data_path", type=str, default="./data/")
    parser.add_argument("--save_path", type=str, default="./logs/")
    parser.add_argument("--text_req", action="store_true")
    parser.add_argument("--data_aug", action="store_true")
    parser.add_argument("--debug", action="store_true")
    parser.add_argument("--seed", type=int, default=212, help="random seed")
    args = parser.parse_args()

    return args


def train_epoch(model, optimizer, epoch, train_loader, device, model_type):
    avg_loss = 0.0
    model.train()
    for i, mini_batch in enumerate(train_loader):
        if model_type == "prediction":
            inputs, targets, mask = mini_batch
        else:
            inputs, targets, mask, text, text_mask = mini_batch
            text = text.to(device)
            text_mask = text_mask.to(device)

        inputs = inputs.to(device)
        targets = targets.to(device)
        mask = mask.to(device)

        batch_size = inputs.shape[0]

        optimizer.zero_grad()

        if model_type == "prediction":
            initial_hidden = model.init_hidden(batch_size, device)
            y_hat, state = model.forward(inputs, initial_hidden)
        else:
            initial_hidden, window_vector, kappa = model.init_hidden(
                batch_size, device)
            y_hat, state, window_vector, kappa = model.forward(
                inputs, text, text_mask, initial_hidden, window_vector, kappa
            )

        loss = compute_nll_loss(targets, y_hat, mask)

        # Output gradient clipping
        y_hat.register_hook(lambda grad: torch.clamp(grad, -100, 100))

        loss.backward()

        # LSTM params gradient clipping
        if model_type == "prediction":
            nn.utils.clip_grad_value_(model.parameters(), 10)
        else:
            nn.utils.clip_grad_value_(model.lstm_1.parameters(), 10)
            nn.utils.clip_grad_value_(model.lstm_2.parameters(), 10)
            nn.utils.clip_grad_value_(model.lstm_3.parameters(), 10)
            nn.utils.clip_grad_value_(model.window_layer.parameters(), 10)

        optimizer.step()
        avg_loss += loss.item()

        # print every 10 mini-batches
        if i % 10 == 0:
            print(
                "[Epoch: {:d}, MiniBatch: {:5d}] loss: {:.3f}".format(
                    epoch + 1, i + 1, loss / batch_size)
            )
    avg_loss /= len(train_loader.dataset)

    return avg_loss


def validation(model, valid_loader, device, epoch, model_type):
    avg_loss = 0.0
    model.eval()

    with torch.no_grad():
        for i, mini_batch in enumerate(valid_loader):
            if model_type == "prediction":
                inputs, targets, mask = mini_batch
            else:
                inputs, targets, mask, text, text_mask = mini_batch
                text = text.to(device)
                text_mask = text_mask.to(device)

            inputs = inputs.to(device)
            targets = targets.to(device)
            mask = mask.to(device)

            batch_size = inputs.shape[0]

            if model_type == "prediction":
                initial_hidden = model.init_hidden(batch_size, device)
                y_hat, state = model.forward(inputs, initial_hidden)
            else:
                initial_hidden, window_vector, kappa = model.init_hidden(
                    batch_size, device
                )
                y_hat, state, window_vector, kappa = model.forward(
                    inputs, text, text_mask, initial_hidden, window_vector,
                    kappa
                )

            loss = compute_nll_loss(targets, y_hat, mask)
            avg_loss += loss.item()

            # print every 10 mini-batches
            if i % 10 == 0:
                print(
                    "[Epoch: {:d}, MB: {:5d}] loss: {:.3f}".format(
                        epoch + 1, i + 1, loss / batch_size
                    )
                )

    avg_loss /= len(valid_loader.dataset)

    return avg_loss


def train(model, train_loader, valid_loader, batch_size, n_epochs, lr,
          patience, step_size, device, model_type, save_path):
    model_path = save_path + "model_" + model_type + ".pt"
    model = model.to(device)
    """
    #TODO
    model.load_state_dict(torch.load(model_path))
    print(f"[INFO] Loaded model weights from '{model_path}'")
    """
    optimizer = optim.Adam(model.parameters(), lr=lr)
    scheduler = StepLR(optimizer, step_size=step_size, gamma=0.1)

    train_losses = []
    valid_losses = []
    best_loss = math.inf
    best_epoch = 0
    k = 0
    for epoch in range(n_epochs):
        start_time = time.time()
        print("[INFO] Training Model.....")
        train_loss = train_epoch(model, optimizer, epoch, train_loader,
                                 device, model_type)

        print("[INFO] Validating Model....")
        valid_loss = validation(model, valid_loader, device, epoch, model_type)

        train_losses.append(train_loss)
        valid_losses.append(valid_loss)

        """
        print(f"Epoch {epoch + 1}: Train: avg. loss: {train_loss:.3f}")
        print(f"Epoch {epoch + 1}: Valid: avg. loss: {valid_loss:.3f}")
        """

        print(f"Epoch {epoch + 1}/{n_epochs}\tTrain loss: {train_loss:.3f}\t"
              f"Val loss: {valid_loss:.3f}")

        if step_size != -1:
            scheduler.step()

        if valid_loss < best_loss:
            best_loss = valid_loss
            best_epoch = epoch + 1
            print("[SAVE] Saving weights at epoch: {}".format(epoch + 1))
            torch.save(model.state_dict(), model_path)
            if model_type == "prediction":
                gen_seq = generate_unconditional_seq(model_path, 700, device,
                                                     bias=10.0, style=None,
                                                     prime=False)

            else:
                gen_seq, phi = generate_conditional_sequence(
                    model_path,
                    "Hello world!",
                    device,
                    train_loader.dataset.char_to_id,
                    train_loader.dataset.idx_to_char,
                    bias=10.0,
                    prime=False,
                    prime_seq=None,
                    real_text=None,
                    is_map=True,
                )

                plt.imshow(phi, cmap="viridis", aspect="auto")
                plt.colorbar()
                plt.xlabel("time steps")
                plt.yticks(np.arange(phi.shape[1]), list("Hello world!  "),
                           rotation="horizontal")
                plt.margins(0.2)
                plt.subplots_adjust(bottom=0.15)
                plt.savefig(save_path + "heat_map" + str(best_epoch) + ".png")
                plt.close()
            # denormalize the generated offsets using train set mean and std
            gen_seq = data_denormalization(
                Global.train_mean, Global.train_std, gen_seq)

            # plot the sequence
            plot_stroke(
                gen_seq[0],
                save_name=save_path + model_type +
                "_seq_" + str(best_epoch) + ".png",
            )
            k = 0
        elif k > patience:
            print("Best model was saved at epoch: {}".format(best_epoch))
            print("Early stopping at epoch {}".format(epoch))
            break
        else:
            k += 1
        print('Time taken per epoch: {:.2f}s\n'.format(time.time() - start_time))


if __name__ == "__main__":

    args = argparser()

    if not os.path.exists(args.save_path):
        os.makedirs(args.save_path)

    # fix random seed
    torch.manual_seed(args.seed)
    np.random.seed(args.seed)

    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

    """
    print("Arguments: {}".format(args))
    """
    print('--ARGUMENTS--')
    for arg in vars(args):
        print(f"{arg} = {getattr(args, arg)}")
    model_type = args.model_type
    batch_size = args.batch_size
    n_epochs = args.n_epochs

    # Load the data and text
    train_dataset = HandwritingDataset(args.data_path, split="train",
                                       text_req=args.text_req,
                                       debug=args.debug,
                                       data_aug=args.data_aug,)

    valid_dataset = HandwritingDataset(args.data_path, split="valid",
                                       text_req=args.text_req,
                                       debug=args.debug,
                                       data_aug=args.data_aug)

    train_loader = DataLoader(
        train_dataset, batch_size=batch_size, shuffle=True)
    valid_loader = DataLoader(
        valid_dataset, batch_size=batch_size, shuffle=False)

    if model_type == "prediction":
        model = HandWritingPredictionNet(
            hidden_size=400, n_layers=3, output_size=121, input_size=3
        )
    elif model_type == "synthesis":
        model = HandWritingSynthesisNet(hidden_size=400, n_layers=3,
                                        output_size=121,
                                        window_size=train_dataset.vocab_size)

    train(model, train_loader, valid_loader, batch_size, n_epochs, args.lr,
          args.patience, args.step_size, device, model_type, args.save_path)
