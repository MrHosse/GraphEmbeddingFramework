import sys
import os
from subprocess import call, DEVNULL
import argparse
import json
import time
import run

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from abstract_embedder import AbstractEmbedder
   
class Struc2Vec(AbstractEmbedder):

    def __init__(self):
        self._name = 'struc2vec'
        self._filename = 'embedding/struc2vec.py'
        self._embpath = 'embedding_result/struc2vec/'
        self._evlpath = 'evaluation_result/'
        
    def create_run(inputs):
        with open('embedding/struc2vec/config.json', 'r') as config_file:
            config = json.load(config_file)
        
        # list of integers
        dim_list = config['dim'] or ['default']
        dim_list = [' -d ' + str(dim) if (dim != 'default') else '' for dim in dim_list]
        
        # list of integers
        walk_len_list = config['walk_len'] or ['default']
        walk_len_list = [' -l ' + str(walk_len) if (walk_len != 'default') else '' for walk_len in walk_len_list]
        
        # list of integers
        num_walks_list = config['num_walks'] or ['default']
        num_walks_list = [' -r ' + str(num_walks) if (num_walks != 'default') else '' for num_walks in num_walks_list]
        
        # list of integers
        win_size_list = config['window_size'] or ['default']
        win_size_list = [' -ws ' + str(win_size) if (win_size != 'default') else '' for win_size in win_size_list]
        
        # list of integers
        until_layer_list = config['until_layer'] or ['default']
        until_layer_list = [' -ul ' + str(until_layer) if (until_layer != 'default') else '' for until_layer in until_layer_list]
        
        # list of integers
        iter_list = config['iter'] or ['default']
        iter_list = [' -i ' + str(iter) if (iter != 'default') else '' for iter in iter_list]
        
        # list of integers
        workers_list = config['workers'] or ['default']
        workers_list = [' -w ' + str(workers) if (workers != 'default') else '' for workers in workers_list]
        
        # list of bools
        opt1_list = config['opt1'] or ['default']
        opt1_list = [' -opt1 ' + str(opt1) if (opt1 != 'default') else '' for opt1 in opt1_list]
        
        # list of bools
        opt2_list = config['opt2'] or ['default']
        opt2_list = [' -opt2 ' + str(opt2) if (opt2 != 'default') else '' for opt2 in opt2_list]
        
        # list of bools
        opt3_list = config['opt3'] or ['default']
        opt3_list = [' -opt3 ' + str(opt3) if (opt3 != 'default') else '' for opt3 in opt3_list]
        
        run.add(
            'layout struc2vec',
            "python embedding/struc2vec/struc2vec.py -src [[edgelist]][[dim]][[walk_len]][[num_walks]][[win_size]]" + 
                "[[until_layer]][[iter]][[workers]][[opt1]][[opt2]][[opt3]]",
            {
             'edgelist': inputs,
             'dim': dim_list,
             'walk_len': walk_len_list,
             'num_walks': num_walks_list,
             'win_size': win_size_list,
             'until_layer': until_layer_list,
             'iter': iter_list,
             'workers': workers_list,
             'opt1': opt1_list,
             'opt2': opt2_list,
             'opt3': opt3_list},
            stdout_file='embedding_result/struc2vec[[dim]][[walk_len]][[num_walks]][[win_size]]' +
                '[[until_layer]][[iter]][[workers]][[opt1]][[opt2]][[opt3]]/[[edgelist]]'
        )

    def calculate_layout(self, 
                         source_graph, 
                         dim=128, 
                         walk_len=80, 
                         num_walks=10, 
                         win_size=10, 
                         until_layer=6, 
                         iter=5, 
                         workers=8,
                         OPT1=False,
                         OPT2=False,
                         OPT3=False,):
        
        cwd = f'embedding/struc2vec/struc2vec_exe/temp/{source_graph}-d{dim}-wl{walk_len}-nw{num_walks}-ws{win_size}-ul{until_layer}-i{iter}-w{workers}-op1{opt1}op2{opt2}op3{opt3}'
        os.makedirs(cwd, exist_ok=True)
        temp_emb_path = 'temp_graph.emb'
        
        temp_graph_path = 'temp_graph'
        mapping = list()
        with open(cwd + '/' + temp_graph_path, 'w') as temp:
            with open(source_graph, 'r') as source:
                for line in source.read().split('\n'):
                    if line == '': continue
                    node0 = line.split(' ')[0]
                    node1 = line.split(' ')[1]

                    if not (node0 in mapping):
                        mapping.append(node0)
                        node0 = len(mapping) - 1
                    else:
                        node0 = mapping.index(node0)
                    if not (node1 in mapping):
                        mapping.append(node1)
                        node1 = len(mapping) - 1
                    else:
                        node1 = mapping.index(node1)

                    temp.write(str(node0) + ' ' + str(node1) + '\n')
        
        args = []
        args.append("python")
        src_path = (len(source_graph.split('/')) + 1) * '../' + 'src/main.py'
        args.append(src_path)
        args.append("--input " + temp_graph_path)
        args.append("--output " + temp_emb_path)
        args.append("--dimensions %d" % dim)
        args.append("--num-walks %d" % num_walks)
        args.append("--walk-length %d" % walk_len)
        args.append("--window-size %d" % win_size)
        args.append("--until-layer %d" % until_layer)
        args.append("--iter %d" % iter)
        args.append("--workers %d" % workers)
        args.append("--OPT1 " + str(OPT1))
        args.append("--OPT2 " + str(OPT2))
        args.append("--OPT3 " + str(OPT3))
        
        call(' '.join(args), stdout=DEVNULL, shell=True, cwd=cwd)
        
        output = '' 
        with open(cwd + '/' + temp_emb_path, 'r') as file:
            contents = file.read().split('\n')
            for line in contents[1:]:
                if line == '': continue
                coord = line.split(' ')
                output += mapping[int(coord[0])] + ',' + ','.join(coord[1:]) + '\n'

        return output
                                
if __name__ == '__main__':
    struc2vec = Struc2Vec()
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-src", "--source_graph", help="path to the edgelist" , type=str)
    parser.add_argument("-d", "--dim", help="Number of dimensions", type=int, default=128)
    parser.add_argument("-l", "--walk_len", help="Length of walk per source", type=int, default=80)
    parser.add_argument("-r", "--num_walks", help="Number of walks per source", type=int, default=10)
    parser.add_argument("-ws", "--window_size", help="Context size for optimization", type=int, default=10)
    parser.add_argument("-ul", "--until_layer", help="Calculation until the layer", type=int, default=6)
    parser.add_argument("-i", "--iter", help="Number of epochs in SGD", type=int, default=5)
    parser.add_argument("-w", "--workers", help="Number of parallel workers", type=int, default=8)
    parser.add_argument("-opt1", "--opt1", help="optimization 1", type=str, default='False')
    parser.add_argument("-opt2", "--opt2", help="optimization 2", type=str, default='False')
    parser.add_argument("-opt3", "--opt3", help="optimization 3", type=str, default='False')
    
    args = parser.parse_args()
    source_graph = args.source_graph
    dim = args.dim
    walk_len = args.walk_len
    num_walks = args.num_walks
    win_size = args.window_size
    until_layer = args.until_layer
    iter = args.iter
    workers = args.workers
    opt1 = bool(args.opt1)
    opt2 = bool(args.opt2)
    opt3 = bool(args.opt3)
        
    t0 = time.time()
    result = struc2vec.calculate_layout(source_graph=source_graph,
                                        dim=dim,
                                        walk_len=walk_len,
                                        num_walks=num_walks,
                                        win_size=win_size,
                                        until_layer=until_layer,
                                        iter=iter,
                                        workers=workers,
                                        OPT1=opt1,
                                        OPT2=opt2,
                                        OPT3=opt3)
    t1 = time.time()
    
    print(source_graph + ' ' + str(t1 - t0))
    print(result)