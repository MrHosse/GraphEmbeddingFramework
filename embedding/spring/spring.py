import sys
import os
import argparse
import json
import time
import run

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from abstract_embedder import AbstractEmbedder
import networkx as nx

class Spring(AbstractEmbedder):

    def __init__(self):
        self._name = 'Fruchterman-Reingold'
        self._filename = 'embedding/spring.py'
        self._embpath = 'embedding_result/spring/'
        self._evlpath = 'evaluation_result/'
    
    @staticmethod
    def spring(inputs):
        with open('embedding/spring/config.json', 'r') as config_file:
            config = json.load(config_file)
        
        # list of dicts or 'default's    
        pos_list = config['pos'] or ['default']
        pos_list = [' -pos ' + json.dumps(pos) if (pos != 'default') else '' for pos in pos_list]
        
        # list of floats
        k_list = config['k'] or ['default']
        k_list = [' -k ' + str(k) if (k != 'default') else '' for k in k_list]
        
        # list of list of nodes
        fixed_list = config['fixed'] or ['default']
        fixed_list = [' -f ' + json.dumps(fixed) if (fixed != 'default') else '' for fixed in fixed_list]
        
        # list of integers
        iter_list = config['iterations'] or ['default']
        iter_list = [' -i ' + str(iter) if (iter != 'default') else '' for iter in iter_list]
        
        # list of floats
        threshold_list = config['threshold'] or ['default']
        threshold_list = [' -t ' + str(threshold) if (threshold != 'default') else '' for threshold in threshold_list]
        
        # list of strings
        weight_list = config['weight'] or ['default']
        weight_list = [' -w ' + weight if (weight != 'default') else '' for weight in weight_list]
        
        # list of floats
        scale_list = config['scale'] or ['default']
        scale_list = [' -s ' + str(scale) if (scale != 'default') else '' for scale in scale_list]
        
        # list of list of coordinates
        center_list = config['center'] or ['default']
        center_list = [' -c ' + json.dumps(center) if (center != 'default') else '' for center in center_list]
        
        # list of integers
        dim_list = config['dim'] or ['default']
        dim_list = [' -d ' + str(dim) if (dim != 'default') else '' for dim in dim_list]
        
        # list of integers
        seed_list = config['seed'] or ['default']
        seed_list = [' -seed ' + str(seed) if (seed != 'default') else '' for seed in seed_list]
        
        run.add(
            'layout spring',
            "python embedding/spring/spring.py -src [[edgelist]][[pos]][[k]][[fixed]][[iteration]]" + 
                "[[threshold]][[weight]][[scale]][[center]][[dim]][[seed]]",
            {
             'edgelist': inputs,
             'pos': pos_list,
             'k': k_list,
             'fixed': fixed_list,
             'iteration': iter_list,
             'threshold': threshold_list,
             'weight': weight_list,
             'scale': scale_list,
             'center': center_list,
             'dim': dim_list,
             'seed': seed_list},
            stdout_file='embedding_result/spring/[[edgelist]][[k]][[fixed]][[iteration]]' +
                '[[threshold]][[weight]][[scale]][[center]][[dim]][[seed]]'
        )
        
    
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
    
    t0 = time.time()
    result = spring.calculate_layout(source_graph=source_graph,
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
    t1 = time.time()
    
    print(source_graph + ' ' + str(t1 - t0))
    print(result)