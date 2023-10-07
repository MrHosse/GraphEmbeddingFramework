import sys
import os
from subprocess import call, DEVNULL
from similarity_metric import EuclidianDistance

from abstract_embedder import AbstractEmbedder
from verse_exe.python.embedding import Embedding
    
class Verse(AbstractEmbedder):

    def __init__(self):
        self._name = 'verse'
        self._filename = 'embedding/verse.py'
        self._embpath = 'embedding_result/verse/'
        self._evlpath = 'evaluation_result/'
        self.similarity_metric = EuclidianDistance
        
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
        
        mapping_path = cwd + '/mapping.csv'
        temp_input = cwd + '/temp_input'
        mapping = dict()
        cnt = 0
        with open(mapping_path, 'w') as map_csv:
            with open(temp_input, 'w') as input:
                with open(source_graph, 'r') as source:
                    for line in source.read().split('\n'):
                        if line == '': continue
                        node0 = line.split(' ')[0]
                        node1 = line.split(' ')[1]

                        if not (node0 in mapping):
                            mapping[node0] = cnt
                            map_csv.write(str(cnt) + ',' + node0 + '\n')
                            cnt += 1
                        node0 = mapping[node0]

                        if not (node1 in mapping):
                            mapping[node1] = cnt
                            map_csv.write(str(cnt) + ',' + node1 + '\n')
                            cnt += 1
                        node1 = mapping[node1]

                        input.write(str(node0) + ' ' + str(node1) + '\n')
                    
        args = []
        args.append("python")
        convert_path = (len(source_graph.split('/')) + 1) * '../' + 'python/convert.py'
        args.append(convert_path)
        args.append("--format edgelist")
        args.append('temp_input')
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
        
        embedding = Embedding(cwd + '/' + tempgraph_path, dim, mapping_path)
        os.makedirs(self._embpath + '/'.join(source_graph.split('/')[:-1]), exist_ok=True)
        
        output = ''
        for node in mapping.keys():
            output += (node + ',' + ','.join(list(map(str, embedding[node]))) + '\n')

        return output
 
if __name__ == '__main__':
    verse = Verse()
    
    print(verse.calculate_layout(source_graph=sys.argv[1]))