import sys
import os
from subprocess import call, DEVNULL
import time

from abstract_embedder import AbstractEmbedder
    
class Struc2Vec(AbstractEmbedder):

    def __init__(self):
        self._name = 'struc2vec'
        self._filename = 'embedding/struc2vec.py'
        self._embpath = 'embedding_result/struc2vec/'
        self._evlpath = 'evaluation_result/'
        
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
        
        cwd = 'embedding/struc2vec_exe/temp/' + source_graph
        os.makedirs(cwd, exist_ok=True)
        tempgraph_path = 'temp_graph.emb'
        
        args = []
        args.append("python")
        src_path = (len(source_graph.split('/')) + 1) * '../' + 'src/main.py'
        args.append(src_path)
        input_path = (len(source_graph.split('/')) + 3) * '../' + source_graph
        args.append("--input " + input_path)
        args.append("--output " + tempgraph_path)
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
        
        os.makedirs(self._embpath + '/'.join(source_graph.split('/')[:-1]), exist_ok=True)
        with open(self._embpath + source_graph, 'w') as f:  
            with open(cwd + '/' + tempgraph_path, 'r') as file:
                contents = file.read().split('\n')
                for line in contents[1:]:
                    f.write(','.join(line.split(' ')) + '\n')
                                
if __name__ == '__main__':
    struc2vec = Struc2Vec()
    
    if not os.path.exists(struc2vec._embpath + sys.argv[1]):
        struc2vec.calculate_layout(source_graph=sys.argv[1])
    
    
    # os.makedirs(struc2vec._evlpath + 'input_data', exist_ok=True)
    # with open(struc2vec._evlpath + sys.argv[1], 'a') as file:
    #     file.write(struc2vec._name + ',')
    #     file.write(str(t1 - t0) + ',')
    #     file.write(str(struc2vec.calculate_avg_edge_length(
    #         edgelist=sys.argv[1], 
    #         embedding=(struc2vec._embpath + sys.argv[1]))) + '\n')