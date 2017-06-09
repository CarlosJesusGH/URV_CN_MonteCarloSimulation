import matplotlib.pyplot as plt
import matplotlib
import settings

def plot_data(x, y, title="title", xlabel="xlabel", ylabel="ylabel", legend=None):
    matplotlib.rcParams.update({'font.size': 18})
    figure = plt.figure(figsize=(12, 9), dpi=100)
    plt.plot(x, y, label=legend)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.grid(True)
    plt.ylim((0, 1))
    plt.xlim((0, 1))
    plt.legend()
    plt.savefig(settings.output_directory_plots + title + ".png")
    # plt.show()
    return figure


def add_plot_to_figure(x, y, figure, title="title", legend=None):
    plt.figure(figure.number)
    plt.plot(x, y, label=legend)
    plt.legend()
    plt.savefig(settings.output_directory_plots + title + ".png")
    return figure


# --------------------------------------------------------------------------
# Other useful tools
# fig = plt.figure(figsize=(12, 6))
# ax = plt.subplot(121)