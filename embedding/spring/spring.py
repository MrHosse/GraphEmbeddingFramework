import sys
import os
import argparse
import json

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from abstract_embedder import AbstractEmbedder
import networkx as nx

class Spring(AbstractEmbedder):

    def __init__(self):
        self._name = 'Fruchterman-Reingold'
        self._filename = 'embedding/spring.py'
        self._embpath = 'embedding_result/spring/'
        self._evlpath = 'evaluation_result/'
        
    def calculate_layout(self, 
                         source_graph,
                         pos,
                         k,
                         fixed,
                         iterations,
                         threshold,
                         weight,
                         scale,
                         center,
                         dim,
                         seed):
        
        graph = nx.read_edgelist(source_graph)

        layout = nx.spring_layout(G=graph,
                                  pos=pos,
                                  k=k,
                                  fixed=fixed,
                                  iterations=iterations,
                                  threshold=threshold,
                                  weight=weight,
                                  scale=scale,
                                  center=center,
                                  dim=dim,
                                  seed=seed)
        
        output = ""
        for key in layout.keys():
            values = layout[key]
            value_str = ','.join(str(value) for value in values)
            line = f"{key},{value_str}\n"
            output += line
        
        return output
        
        
if __name__ == '__main__':
    spring = Spring()
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-src", "--source_graph", help="path to the edgelist" , type=str)
    parser.add_argument("-k", "--k_value", help="Optimal distance between nodes", type=float)
    parser.add_argument("-pos", "--position", help="initial position of nodes as JSON", type=str)
    parser.add_argument("-f", "--fixed", help="Nodes to keep fixed at initial position as a list", type=str)
    parser.add_argument("-i", "--iterations", help="Maximum number of iterations", type=int, default=50)
    parser.add_argument("-t", "--threshold", help="Threshold for relative error in node position changes", type=float, default=1e-4)
    parser.add_argument("-w", "--weight", help="The edge attribute that holds the numerical value used for edge weight", type=str, default="weight")
    parser.add_argument("-s", "--scale", help="Scale factor for positions", type=float, default=1.0)
    parser.add_argument("-c", "--center", help="Coordinate pair around which to center the layout", type=str)
    parser.add_argument("-d", "--dim", help="Dimension of layout", type=int, default=2)
    parser.add_argument("-seed", "--seed", help="Set the random seed for deterministic node layouts", type=int)
    
    args = parser.parse_args()
    print(args)
    source_graph = args.source_graph
    pos = None if args.position is None else json.loads(args.position)
    k = args.k_value
    fixed = None if args.fixed is None else json.loads(args.fixed)
    iterations = args.iterations
    threshold = args.threshold
    weight = args.weight
    scale = args.scale
    center = None if args.center is None else json.loads(args.center)
    dim = args.dim
    seed = args.seed
    
    print(spring.calculate_layout(source_graph=source_graph,
                                  pos=pos,
                                  k=k,
                                  fixed=fixed,
                                  iterations=iterations,
                                  threshold=threshold,
                                  weight=weight,
                                  scale=scale,
                                  center=center,
                                  dim=dim,
                                  seed=seed))