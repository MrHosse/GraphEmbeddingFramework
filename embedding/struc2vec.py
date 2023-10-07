import sys
import os
from subprocess import call, DEVNULL

from abstract_embedder import AbstractEmbedder
from similarity_metric import EuclidianDistance
   
class Struc2Vec(AbstractEmbedder):

    def __init__(self):
        self._name = 'struc2vec'
        self._filename = 'embedding/struc2vec.py'
        self._embpath = 'embedding_result/struc2vec/'
        self._evlpath = 'evaluation_result/'
        self.similarity_metric = EuclidianDistance

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
        
        output = '' 
        with open(cwd + '/' + tempgraph_path, 'r') as file:
            contents = file.read().split('\n')
            for line in contents[1:]:
                output += (','.join(line.split(' ')) + '\n')

        return output
                                
if __name__ == '__main__':
    struc2vec = Struc2Vec()
    
    print(struc2vec.calculate_layout(source_graph=sys.argv[1]))