import pathlib
import pickle

import matplotlib.pyplot as plt
from keras.src.callbacks import History


def save_plot(stamp: str, title: str, history: History, dir_path: pathlib.Path):
    #dbg
    with open('history.pkl', 'wb') as f:
        pickle.dump(history, f)
    #dbg
    plt.clf()
    fig, axes = plt.subplots(2, 2)

    fig.suptitle(f"{stamp} {title}")

    # train displays "Epoch 1/7", so let the plot starts from 1
    x = [x + 1 for x in history.epoch]

    for idx, characteristic in enumerate(["loss", "binary_accuracy", "precision", "recall"]):
        axes_x = (1 & idx)
        axes_y = (2 & idx) >> 1
        y_train = history.history[characteristic]
        y_test = history.history[f"val_{characteristic}"]
        axes[axes_x, axes_y].plot(x, y_train, label="train")
        axes[axes_x, axes_y].plot(x, y_test, label="test")
        axes[axes_x, axes_y].set_title(characteristic)
        axes[axes_x, axes_y].legend(loc="upper left")
        axes[axes_x, axes_y].grid(visible=True, which="both", color="grey", linewidth=0.75, linestyle="dotted")
        axes[axes_x, axes_y].set_xticks(range(min(x), max(x) + 1, 1), minor=True)

    plt.gcf().set_size_inches(16, 9)
    plt.savefig(dir_path / f"{stamp}.png", dpi=96)


# dbg
if __name__ == "__main__":
    _dir_path = pathlib.Path("results")
    current_time = "20240321_190401"
    with open(f"results/history-{current_time}.pickle", "rb") as f:
        fit_history = pickle.load(f)
    save_plot(current_time, fit_history, _dir_path)
