import matplotlib.pyplot as plt
import settings

def plot_data(x, y, title="title", xlabel="xlabel", ylabel="ylabel"):
    fig = plt.figure()
    plt.plot(x, y)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.grid(True)
    plt.ylim((0, 1))
    plt.xlim((0, 1))
    plt.savefig(settings.output_directory_plots + title + ".png")
    # plt.show()


# fig = plt.figure(figsize=(12, 6))
# ax = plt.subplot(121)