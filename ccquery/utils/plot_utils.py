import matplotlib.pyplot as plt

from ccquery.error import ConfigError
from ccquery.utils import io_utils

def length_plot(output, data, title, xlabel, ylabel, figsize=(15, 6)):
    """Draw the bars for query's length in number of words/chars"""

    if not isinstance(data, dict):
        raise ConfigError(
            "Method expects a dict object instead of {}".format(data.__class__))

    io_utils.create_path(output)

    plt.figure(figsize=figsize)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.bar(
        data.keys(),
        data.values(),
        linewidth=1,
        width=1,
        color='g',
        edgecolor='black')

    if len(data) < 30:
        plt.xticks(list(data.keys()))

    plt.savefig(output)
    plt.close()

def occurrences_plot(
        output, data, mins,
        title, xlabel, ylabel,
        left_lim=None, right_lim=None, text_style=None, figsize=(15, 6)):
    """
    Draw the number of unique words and the coverage of words
    when applying a minimum number of occurrences filter
    """

    if not isinstance(data, list):
        raise ConfigError(
            "Method expects a list object instead of {}".format(data.__class__))

    mins = sorted(mins)

    # recover counts
    ntokens = 0
    counts = {minvalue: 0 for minvalue in mins}
    coverage = {minvalue: 0 for minvalue in mins}
    for x in data:
        ntokens += x
        for minvalue in mins:
            if x >= minvalue:
                counts[minvalue] += 1
                coverage[minvalue] += x

    for minvalue, count in coverage.items():
        coverage[minvalue] = round(100.0 * count / ntokens, 2)

    x = list(range(len(mins)))
    xticks = ["min{:.3g}occ".format(minvalue) for minvalue in mins]

    # draw plot with two scales: one for counts, one for coverage
    if not text_style:
        text_style = dict(
            ha='center', va='bottom', linespacing=0.3,
            fontsize=10, family='monospace')

    fig, ax1 = plt.subplots(figsize=figsize)

    # counts axis
    color = 'green'
    y = [counts[minvalue] for minvalue in mins]
    ax1.set_title(title)
    ax1.set_xlabel(xlabel)
    ax1.set_ylabel(ylabel)
    ax1.set_xticks(x)
    ax1.set_xticklabels(xticks)
    if left_lim:
        ax1.set_ylim(left_lim)
    ax1.tick_params(axis='y', labelcolor=color)
    ax1.bar(x, y, linewidth=1, width=1, color=color, edgecolor='black')
    for i, j in zip(x, y):
        ax1.annotate(str(j) + '\n', xy=(i, j), **text_style)

    # coverage axis
    text_style['ha'] = 'left'

    color = 'blueviolet'
    y = [coverage[minvalue] for minvalue in mins]
    ax2 = ax1.twinx()
    if right_lim:
        ax2.set_ylim(right_lim)
    else:
        ax2.set_ylim([50, 110])
    ax2.set_ylabel('Coverage [%]')
    ax2.tick_params(axis='y', labelcolor=color)
    ax2.plot(x, y, color=color, linestyle=':', marker='o')
    for i, j in zip(x, y):
        ax2.annotate(str(j) + '%\n', xy=(i, j), **text_style)

    fig.tight_layout()
    plt.savefig(output)
    plt.close()
