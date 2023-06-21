import os
from pathlib import Path
import networkx as nx
import matplotlib.pyplot as plt
from gem.embedding import node2vec

def draw(sourcepath, targetpath, name):
    """
    Uses an implementation of node2vec to draw the graph located at the given sourcepath
    and saves it in the targetpath
    """
    graph = nx.read_edgelist(sourcepath)
    options = {
        'node_color': 'black',
        'node_size': 100,
        'width': 1,
    }
    plt.clf()
    subax1 = plt.subplot(111)

    node2vec = Node2Vec(graph, dimensions=64, walk_length=30, num_walks=200, workers=1)
    model = node2vec.fit(window=10, min_count=1, batch_words=4)
    model.wv.most_similar

    savepath = os.path.join(targetpath, 'spring', name + ".png")
    Path(savepath).parent.mkdir(exist_ok=True, parents=True)
    plt.savefig(savepath)