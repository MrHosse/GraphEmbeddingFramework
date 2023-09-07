import sys
import os
import time

from abstract_embedder import AbstractEmbedder

import networkx as nx
import numpy as np
import scipy.sparse.linalg as lg

from gem.embedding.hope import HOPE
from gem.utils import graph_util

class Hope(AbstractEmbedder):
    
    def __init__(self):
        self._name = 'HOPE'
        self._filename = 'embedding/hope.py'
        self._embpath = 'embedding_result/hope/'
        self._evlpath = 'evaluation_result/'
        
    def calculate_layout(self, source_graph, dim=4, beta=0.01):
        
        graph = graph_util.loadGraphFromEdgeListTxt(source_graph, directed=True)
        graph = graph.to_directed()
        
        A = nx.to_numpy_matrix(graph)
        m_g = np.eye(len(graph.nodes)) - beta * A
        m_l = beta * A
        S = np.dot(np.linalg.inv(m_g), m_l)

        u, s, vt = lg.svds(S, k=dim // 2)
        X1 = np.dot(u, np.diag(np.sqrt(s)))
        X2 = np.dot(vt.T, np.diag(np.sqrt(s)))
        X = np.concatenate((X1, X2), axis=1)
        
        os.makedirs(self._embpath + 'input_data', exist_ok=True)
        with open(self._embpath + sys.argv[1], 'w') as file:
            output = ""
            for i in range(len(X)):
                j = i + 1
                output += f"{str(j)},{','.join(str(value) for value in X[i])}\n"
            file.write(output)
        

        #p_d_p_t = np.dot(u, np.dot(np.diag(s), vt))
        #eig_err = np.linalg.norm(p_d_p_t - S)
        
if __name__ == '__main__':
    hope = Hope()
    
    hope.calculate_layout(source_graph=sys.argv[1])
    
    # os.makedirs(hope._evlpath + 'input_data', exist_ok=True)
    # with open(hope._evlpath + sys.argv[1], 'a') as file:
    #     file.write(hope._name + ',')
    #     file.write(str(t1 - t0) + ',')
    #     file.write(str(
    #         hope.calculate_avg_edge_length(edgelist=sys.argv[1], 
    #         embedding=(hope._embpath + sys.argv[1]))) + '\n')        
        