import sys
import os
from subprocess import call
from subprocess import DEVNULL
import time

from abstract_embedder import AbstractEmbedder

from gem.utils import graph_util
    
class Node2Vec(AbstractEmbedder):

    def __init__(self):
        self._name = 'node2vec'
        self._filename = 'embedding/node2vec.py'
        self._embpath = 'embedding_result/node2vec/'
        self._evlpath = 'evaluation_result/'
        
    def calculate_layout(self, source_graph, dim=4, max_iter=1, walk_len=80, num_walks=10, con_size=10, ret_p=1, inout_p=1):
        
        current_dir = os.path.dirname(os.path.abspath(__file__))
        executable = os.path.abspath(os.path.join(current_dir, 'node2vec_exe/node2vec'))
        
        args = [executable]
        graph = graph_util.loadGraphFromEdgeListTxt(source_graph)
        graph_util.saveGraphToEdgeListTxtn2v(graph, os.path.abspath(os.path.join(current_dir, 'node2vec_exe/' + source_graph + '.graph')))
        args.append("-i:" + os.path.abspath(os.path.join(current_dir, 'node2vec_exe/' + source_graph + '.graph')))
        args.append("-o:" + os.path.abspath(os.path.join(current_dir, 'node2vec_exe/' + source_graph + '.emb')))
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
        
        os.makedirs(self._embpath + 'input_data', exist_ok=True)
        with open(self._embpath + sys.argv[1], 'w') as f:   
            with open(os.path.abspath(os.path.join(current_dir, 'node2vec_exe/' + source_graph + '.emb')), 'r') as file:
                contents = file.read().split('\n')
                for line in contents[1:]:
                    f.write(','.join(line.split(' ')) + '\n')
                    
        os.remove(os.path.abspath(os.path.join(current_dir, 'node2vec_exe/' + source_graph + '.graph')))
        os.remove(os.path.abspath(os.path.join(current_dir, 'node2vec_exe/' + source_graph + '.emb')))
        
        
if __name__ == '__main__':
    node2vec = Node2Vec()
    
    t0 = time.time()
    node2vec.calculate_layout(source_graph=sys.argv[1])
    t1 = time.time()
    
    os.makedirs(node2vec._evlpath + 'input_data', exist_ok=True)
    with open(node2vec._evlpath + sys.argv[1], 'a') as file:
        file.write(node2vec._name + ',')
        file.write(str(t1 - t0) + ',')
        file.write(str(
            node2vec.calculate_avg_edge_length(edgelist=sys.argv[1], 
            embedding=(node2vec._embpath + sys.argv[1]))) + '\n')