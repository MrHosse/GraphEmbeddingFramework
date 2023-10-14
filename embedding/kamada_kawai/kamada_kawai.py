import sys
import os
import argparse
import json
import time
import run

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from abstract_embedder import AbstractEmbedder
import networkx as nx

class KamadaKawai(AbstractEmbedder):

    def __init__(self):
        self._name = 'Kamada-Kawai'
        self._filename = 'embedding/kamada_kawai.py'
        self._embpath = 'embedding_result/kamada_kawai/'
        self._evlpath = 'evaluation_result/'

    def create_run(inputs):
        with open('embedding/kamada_kawai/config.json', 'r') as config_file:
            config = json.load(config_file)
        
        # list of 2 layer dicts or 'default'  
        dist_list = config['dist'] or ['default']
        dist_list = [' -dist ' + json.dumps(dist) if (dist != 'default') else '' for dist in dist_list]
        
        # list of dicts or 'default'
        pos_list = config['pos'] or ['default']
        pos_list = [' -pos ' + json.dumps(pos) if (pos != 'default') else '' for pos in pos_list]
        
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
        
        run.add(
            'layout kamada_kawai',
            "python embedding/kamada_kawai/kamada_kawai.py -src [[edgelist]][[dist]][[pos]]" + 
                "[[weight]][[scale]][[center]][[dim]]",
            {
             'edgelist': inputs,
             'dist': dist_list,
             'pos': pos_list,
             'weight': weight_list,
             'scale': scale_list,
             'center': center_list,
             'dim': dim_list},
            stdout_file='embedding_result/kamada_kawai/[[edgelist]][[dist]][[pos]]' +
                '[[weight]][[scale]][[center]][[dim]]'
        )

    def calculate_layout(self, 
                         source_graph,
                         dist,
                         pos,
                         weight,
                         scale,
                         center,
                         dim):
        
        graph = nx.read_edgelist(source_graph)

        layout = nx.kamada_kawai_layout(G=graph,
                                        dist=dist,
                                        pos=pos,
                                        weight=weight,
                                        scale=scale,
                                        center=center,
                                        dim=dim)
        
        os.makedirs(self._embpath + '/'.join(source_graph.split('/')[:-1]), exist_ok=True)
        
        output = ""
        for key in layout.keys():
            values = layout[key]
            value_str = ','.join(str(value) for value in values)
            line = f"{key},{value_str}\n"
            output += line
        
        return output
            
        
if __name__ == '__main__':
    kamada_kawai = KamadaKawai()
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-src", "--source_graph", help="path to the edgelist" , type=str)
    parser.add_argument("-dist", "--dist", help="optimal distances between nodes as JSON (2 layer dict)", type=str)
    parser.add_argument("-pos", "--position", help="initial position of nodes as JSON", type=str)
    parser.add_argument("-w", "--weight", help="The edge attribute that holds the numerical value used for edge weight", type=str, default="weight")
    parser.add_argument("-s", "--scale", help="Scale factor for positions", type=float, default=1.0)
    parser.add_argument("-c", "--center", help="Coordinate pair around which to center the layout", type=str)
    parser.add_argument("-d", "--dim", help="Dimension of layout", type=int, default=2)
    
    args = parser.parse_args()
    source_graph = args.source_graph
    dist = None if args.dist is None else json.loads(args.dist)
    pos = None if args.position is None else json.loads(args.position)
    weight = args.weight
    scale = args.scale
    center = None if args.center is None else json.loads(args.center)
    dim = args.dim
    
    t0 = time.time()
    result = kamada_kawai.calculate_layout(source_graph=source_graph,
                                           dist=dist,
                                           pos=pos,
                                           weight=weight,
                                           scale=scale,
                                           center=center,
                                           dim=dim)
    t1 = time.time()
    
    print(source_graph + ' ' + str(t1 - t0))
    print(result)