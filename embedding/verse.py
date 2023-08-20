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
        convert_path = (len(source_graph.split('/')) + 1) * '../' + 'python/convert.py'
        args.append(convert_path)
        args.append("--format edgelist")
        relativ_source_path = (len(source_graph.split('/')) + 3) * '../' + source_graph
        args.append(relativ_source_path)
        args.append(temp_bcsr)
        
        call(' '.join(args), stdout=DEVNULL, shell=True, cwd=cwd)
        
        args = []
        src_path = (len(source_graph.split('/')) + 1) * '../' + 'src/verse'
        args.append(src_path)
        args.append("-input " + temp_bcsr)
        args.append("-output " + tempgraph_path)
        args.append("-dim %d" % dim)
        args.append("-alpha " + str(alpha))
        args.append("-threads %d" % threads)
        args.append("-nsamples %d" % nsamples)
        
        call(' '.join(args), stdout=DEVNULL, shell=True, cwd=cwd)
        
        embedding = Embedding(cwd + '/' + tempgraph_path, dim)
        os.makedirs(self._embpath + '/'.join(source_graph.split('/')[:-1]), exist_ok=True)
        
        with open(self._embpath + source_graph, 'w') as f:
            embeddings = embedding.embeddings  
            for i in range(len(embeddings)):
                f.write(str(i) + ',' + ','.join(list(map(str, embeddings[i]))) + '\n')
        
 
if __name__ == '__main__':
    verse = Verse()
    
    t0 = time.time()
    if not os.path.exists(verse._embpath + sys.argv[1]):
        verse.calculate_layout(source_graph=sys.argv[1])
    t1 = time.time()
    
    
    # os.makedirs(struc2vec._evlpath + 'input_data', exist_ok=True)
    # with open(struc2vec._evlpath + sys.argv[1], 'a') as file:
    #     file.write(struc2vec._name + ',')
    #     file.write(str(t1 - t0) + ',')
    #     file.write(str(struc2vec.calculate_avg_edge_length(
    #         edgelist=sys.argv[1], 
    #         embedding=(struc2vec._embpath + sys.argv[1]))) + '\n')