import pandas as pd
import matplotlib.pyplot as plt

def make_graph(csv_file, x_axis, y_axis, 
        title="", x_name="", y_name="", 
        x_range=None, y_range=None,
        output_file=""):

    df = pd.read_csv(csv_file, sep='\t')

    plt.plot(df['episode'], df['rate'], )

    if not x_name:
        x_name = x_axis
    if not y_name:
        y_name = y_axis
    plt.xlabel(x_name)
    plt.ylabel(y_name)

    plt.tick_params(axis="x", direction="in")
    plt.tick_params(axis="y", direction="in")
    if title:
        plt.title(title)
    if x_range:
        plt.xlim(x_range)
    if y_range:
        plt.ylim(y_range)
    if output_file:
        plt.savefig(output_file)
    else:
        plt.savefig(f"{csv_file}.png")

if __name__ == "__main__":
    make_graph(
        csv_file = "./progress_300000.txt",
        x_axis = "episode",
        y_axis = "rate",
        title = "Learning Curve",
        y_name = "Win Rate (vs Random computer)",
        x_range = [0, 300000],
        y_range = [0, 1],
        output_file = "./progress_300000.png",
    )
