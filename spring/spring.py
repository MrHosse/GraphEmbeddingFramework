import os
from pathlib import Path
import networkx as nx
import matplotlib.pyplot as plt
from time import time
from gem.evaluation import visualize_embedding as viz

def draw(sourcepath, targetpath, name):
    """
    Uses the algorithm by Fruchterman-Reingold to draw the graph located at the given sourcepath
    and saves it in the targetpath
    """
    graph = nx.read_edgelist(sourcepath)
    options = {
        'node_color': 'black',
        'node_size': 100,
        'width': 1,
    }

    print('Number of nodes: %d, number of edges: %d' % (graph.number_of_nodes(), graph.number_of_edges()))
    t = time()

    nx.draw_networkx(graph, **options)
    plt.title('%s using Fruchtermann-Reingold:' % (name), loc= 'left')

    print('Time needed: %f' % (time() - t))
    
    savepath = os.path.join(targetpath, 'spring', name + ".png")
    Path(savepath).parent.mkdir(exist_ok=True, parents=True)
    plt.savefig(savepath)
    plt.clf()