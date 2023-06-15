import os
from pathlib import Path
import networkx as nx
import matplotlib.pyplot as plt
from time import time

def draw(sourcepath, targetpath, name):
    """
    Uses the algorithm by Kamada-Kawai to draw the graph located at the given sourcepath
    and saves it in the targetpath
    """
    graph = nx.read_edgelist(sourcepath)
    options = {
        'node_color': 'black',
        'node_size': 100,
        'width': 1,
    }

    t = time()

    nx.draw_networkx(graph, **options)
    
    print('Method: Kamada-Kawai on %s' % (name))
    print('Number of nodes: %d, number of edges: %d' % (graph.number_of_nodes(), graph.number_of_edges()))
    print('Time needed: %f' % (time() - t))
    print("\n"+'-'*80)
    
    savepath = os.path.join(targetpath, 'kamada_kawai', name + ".png")
    Path(savepath).parent.mkdir(exist_ok=True, parents=True)
    plt.savefig(savepath)
    plt.clf()