import sys
import os
from subprocess import call
from subprocess import DEVNULL
import networkx as nx

from abstract_embedder import AbstractEmbedder
    
class Node2Vec(AbstractEmbedder):

    def __init__(self):
        self._name = 'node2vec'
        self._filename = 'embedding/node2vec.py'
        self._embpath = 'embedding_result/node2vec/'
        self._evlpath = 'evaluation_result/'
    
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
        
        executable = 'embedding/snap/examples/node2vec/node2vec'
        temp_dir = 'embedding/node2vec_exe/' + source_graph
        os.makedirs(temp_dir, exist_ok=True)
        temp_graph_path = temp_dir + '/temp.graph'
        temp_emb_path = temp_dir + '/temp.emb'
        
        args = [executable]
        
        graph = Node2Vec.loadGraphFromEdgeListTxt(source_graph)
        Node2Vec.saveGraphToEdgeListTxtn2v(graph, temp_graph_path)
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
                output += ','.join(line.split(' ')) + '\n'
                
        
        
        return output
        
        
if __name__ == '__main__':
    node2vec = Node2Vec()

    print(node2vec.calculate_layout(source_graph=sys.argv[1]))