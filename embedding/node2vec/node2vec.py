import sys
import os
import argparse
import json
import time
import run

from subprocess import call
from subprocess import DEVNULL
import networkx as nx

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from abstract_embedder import AbstractEmbedder
    
class Node2Vec(AbstractEmbedder):

    def __init__(self):
        self._name = 'node2vec'
        self._filename = 'embedding/node2vec.py'
        self._embpath = 'embedding_result/node2vec/'
        self._evlpath = 'evaluation_result/'
    
    def loadGraphFromEdgeListTxt(file_name, directed=False):
        with open(file_name, 'r') as f:
            # n_nodes = f.readline()
            # f.readline() # Discard the number of edges
            if directed:
                G = nx.DiGraph()
            else:
                G = nx.Graph()
            for line in f:
                edge = line.strip().split()
                if len(edge) == 3:
                    w = float(edge[2])
                else:
                    w = 1.0
                G.add_edge(int(edge[0]), int(edge[1]), weight=w)
        return G
    
    def saveGraphToEdgeListTxtn2v(graph, file_name):
        with open(file_name, 'w') as f:
            for i, j, w in graph.edges(data='weight', default=1):
                f.write('%d %d %f\n' % (i, j, w))

    def create_run(inputs):
        with open('embedding/node2vec/config.json', 'r') as config_file:
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
        con_size_list = config['con_size'] or ['default']
        con_size_list = [' -k ' + str(con_size) if (con_size != 'default') else '' for con_size in con_size_list]
        
        # list of integers
        max_iter_list = config['max_iter'] or ['default']
        max_iter_list = [' -e ' + str(max_iter) if (max_iter != 'default') else '' for max_iter in max_iter_list]
        
        # list of floats
        ret_p_list = config['ret_p'] or ['default']
        ret_p_list = [' -p ' + str(ret_p) if (ret_p != 'default') else '' for ret_p in ret_p_list]
        
        # list of floats
        inout_p_list = config['inout_p'] or ['default']
        inout_p_list = [' -q ' + str(inout_p) if (inout_p != 'default') else '' for inout_p in inout_p_list]
        
        run.add(
            'layout node2vec',
            "python embedding/node2vec/node2vec.py -src [[edgelist]][[dim]][[walk_len]][[num_walks]][[con_size]]" + 
                "[[max_iter]][[ret_p]][[inout_p]]",
            {
             'edgelist': inputs,
             'dim': dim_list,
             'walk_len': walk_len_list,
             'num_walks': num_walks_list,
             'con_size': con_size_list,
             'max_iter': max_iter_list,
             'ret_p': ret_p_list,
             'inout_p': inout_p_list},
            stdout_file='embedding_result/node2vec[[dim]][[walk_len]][[num_walks]][[con_size]]' +
                '[[max_iter]][[ret_p]][[inout_p]]/[[edgelist]]'
        )
    
    def calculate_layout(self, 
                         source_graph, 
                         dim=128, 
                         walk_len=80, 
                         num_walks=10, 
                         con_size=10,
                         max_iter=1,
                         ret_p=1, 
                         inout_p=1):
        
        executable = 'embedding/snap/examples/node2vec/node2vec'
        temp_dir = f'embedding/node2vec/temp/{source_graph} -d {dim} -l {walk_len} -r {num_walks} -k {con_size} -e {max_iter} -p {ret_p} -q {inout_p}'
        os.makedirs(temp_dir, exist_ok=True)
        temp_graph_path = temp_dir + '/temp.graph'
        temp_emb_path = temp_dir + '/temp.emb'
        
        args = [executable]
        
        mapping = list()
        graph = nx.Graph()
        with open(source_graph, 'r') as source:
            for line in source:
                if line == '': continue
                edge = line.strip().split()
                if len(edge) == 3:
                    w = float(edge[2])
                else:
                    w = 1.0
                
                node0 = edge[0]
                node1 = edge[1]
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
                
                graph.add_edge(node0, node1, weight=w)
        
        with open(temp_graph_path, 'w') as f:
            for i, j, w in graph.edges(data='weight', default=1):
                f.write('%d %d %f\n' % (i, j, w))
        
        args.append("-i:" + temp_graph_path)
        
        args.append("-o:" + temp_emb_path)
        args.append("-d:%d" % dim)
        args.append("-l:%d" % walk_len)
        args.append("-r:%d" % num_walks)
        args.append("-k:%d" % con_size)
        args.append("-e:%d" % max_iter)
        args.append("-p:%f" % ret_p)
        args.append("-q:%f" % inout_p)
        args.append("-dr")
        args.append("-w")
        
        call(args, stdout=DEVNULL)
        
        output = ''   
        with open(temp_emb_path, 'r') as file:
            contents = file.read().split('\n')
            for line in contents[1:]:
                if line == '': continue
                coord = line.split(' ')
                output += mapping[int(coord[0])] + ',' + ','.join(coord[1:]) + '\n'
                
        return output
        
        
if __name__ == '__main__':
    node2vec = Node2Vec()
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-src", "--source_graph", help="path to the edgelist" , type=str)
    parser.add_argument("-d", "--dim", help="Number of dimensions", type=int, default=128)
    parser.add_argument("-l", "--walk_len", help="Length of walk per source", type=int, default=80)
    parser.add_argument("-r", "--num_walks", help="Number of walks per source", type=int, default=10)
    parser.add_argument("-k", "--con_size", help="Context size for optimization", type=int, default=10)
    parser.add_argument("-e", "--max_iter", help="Number of epochs in SGD", type=int, default=1)
    parser.add_argument("-p", "--ret_p", help="Return hyperparameter", type=int, default=1)
    parser.add_argument("-q", "--inout_p", help="Inout hyperparameter", type=int, default=1)
    
    args = parser.parse_args()
    source_graph = args.source_graph
    dim = args.dim
    walk_len = args.walk_len
    num_walks = args.num_walks
    con_size = args.con_size
    max_iter = args.max_iter
    ret_p = args.ret_p
    inout_p = args.inout_p

    t0 = time.time()
    result = node2vec.calculate_layout(source_graph=source_graph,
                                       dim=dim,
                                       walk_len=walk_len,
                                       num_walks=num_walks,
                                       con_size=con_size,
                                       max_iter=max_iter,
                                       ret_p=ret_p,
                                       inout_p=inout_p)
    t1 = time.time()
    
    print(source_graph + ' ' + str(t1 - t0))
    print(result)