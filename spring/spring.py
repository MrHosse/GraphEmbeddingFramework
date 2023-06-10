import os
from pathlib import Path
import networkx as nx
import matplotlib.pyplot as plt

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

    plt.clf()
    subax1 = plt.subplot(111)
    nx.draw(graph, **options)
    
    savepath = os.path.join(targetpath, 'spring', name + ".png")
    Path(savepath).parent.mkdir(exist_ok=True, parents=True)
    plt.savefig(savepath)