import sys
import os
from subprocess import call
from subprocess import DEVNULL
from similarity_metric import EuclidianDistance
import networkx as nx

from abstract_embedder import AbstractEmbedder
    
class Node2Vec(AbstractEmbedder):

    def __init__(self):
        self._name = 'node2vec'
        self._filename = 'embedding/node2vec.py'
        self._embpath = 'embedding_result/node2vec/'
        self._evlpath = 'evaluation_result/'
        self.similarity_metric = EuclidianDistance
    
    def loadGraphFromEdgeListTxt(file_name, directed=True):
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

    def calculate_layout(self, source_graph, dim=128, max_iter=1, walk_len=80, num_walks=10, con_size=10, ret_p=1, inout_p=1):
        
        current_dir = os.path.dirname(os.path.abspath(__file__))
        executable = os.path.abspath(os.path.join(current_dir, 'node2vec_exe/node2vec'))
        
        args = [executable]
        graph = Node2Vec.loadGraphFromEdgeListTxt(source_graph)
        os.makedirs('embedding/node2vec_exe/' + '/'.join(source_graph.split('/')[:-1]), exist_ok=True)
        Node2Vec.saveGraphToEdgeListTxtn2v(graph, os.path.abspath(os.path.join(current_dir, 'node2vec_exe/' + source_graph + '.graph')))
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
        
        os.makedirs(self._embpath + '/'.join(source_graph.split('/')[:-1]), exist_ok=True)
        with open(self._embpath + source_graph, 'w') as f:   
            with open(os.path.abspath(os.path.join(current_dir, 'node2vec_exe/' + source_graph + '.emb')), 'r') as file:
                contents = file.read().split('\n')
                for line in contents[1:]:
                    f.write(','.join(line.split(' ')) + '\n')
                    
        os.remove(os.path.abspath(os.path.join(current_dir, 'node2vec_exe/' + source_graph + '.graph')))
        os.remove(os.path.abspath(os.path.join(current_dir, 'node2vec_exe/' + source_graph + '.emb')))
        
        
if __name__ == '__main__':
    node2vec = Node2Vec()
    
    if not os.path.exists(node2vec._embpath + sys.argv[1]):
        node2vec.calculate_layout(source_graph=sys.argv[1])
    
    node2vec.save_info()