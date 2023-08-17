import sys
import os
from subprocess import call, DEVNULL
import time

from abstract_embedder import AbstractEmbedder
from verse_exe.python.embedding import Embedding
    
class Verse(AbstractEmbedder):

    def __init__(self):
        self._name = 'verse'
        self._filename = 'embedding/verse.py'
        self._embpath = 'embedding_result/verse/'
        self._evlpath = 'evaluation_result/'
        
    def calculate_layout(self, 
                         source_graph, 
                         dim=128, 
                         alpha=0.85,
                         threads=4,
                         nsamples=3):
        
        cwd = 'embedding/verse_exe/temp/' + source_graph
        os.makedirs(cwd, exist_ok=True)
        tempgraph_path = 'temp_graph.bin'
        temp_bcsr = 'temp_bscr.bscr'
        
        args = []
        args.append("python")
        args.append("../../../python/convert.py")
        args.append("--format edgelist")
        args.append("../../../../../" + source_graph)
        args.append(temp_bcsr)
        
        call(' '.join(args), stdout=DEVNULL, shell=True, cwd=cwd)
        
        args = []
        args.append('../../../src/verse')
        args.append("-input " + temp_bcsr)
        args.append("-output " + tempgraph_path)
        args.append("-dim %d" % dim)
        args.append("-alpha " + str(alpha))
        args.append("-threads %d" % threads)
        args.append("-nsamples %d" % nsamples)
        
        call(' '.join(args), stdout=DEVNULL, shell=True, cwd=cwd)
        
        embedding = Embedding(cwd + '/' + tempgraph_path, dim)
        print(embedding.load_embeddings(cwd + '/' + tempgraph_path))
        
        """
        os.makedirs(self._embpath + 'input_data', exist_ok=True)
        with open(self._embpath + sys.argv[1], 'w') as f:  
            with open(cwd + '/' + tempgraph_path, 'r') as file:
                contents = file.read().split('\n')
                for line in contents[1:]:
                    f.write(','.join(line.split(' ')) + '\n')
        """
 
if __name__ == '__main__':
    verse = Verse()
    
    t0 = time.time()
    verse.calculate_layout(source_graph=sys.argv[1])
    t1 = time.time()
    
    
    # os.makedirs(struc2vec._evlpath + 'input_data', exist_ok=True)
    # with open(struc2vec._evlpath + sys.argv[1], 'a') as file:
    #     file.write(struc2vec._name + ',')
    #     file.write(str(t1 - t0) + ',')
    #     file.write(str(struc2vec.calculate_avg_edge_length(
    #         edgelist=sys.argv[1], 
    #         embedding=(struc2vec._embpath + sys.argv[1]))) + '\n')