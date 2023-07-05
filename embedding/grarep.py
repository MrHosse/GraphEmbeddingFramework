import sys
import os
from subprocess import call

from abstract_embedder import AbstractEmbedder
    
class GraRep(AbstractEmbedder):

    def __init__(self):
        self._name = 'GraRep'
        self._filename = 'embedding/grarep.py'
        
    def calculate_layout(self, source_graph, 
                         dim=16, 
                         order=5, 
                         iterations=20,  
                         seed=40):
        
        current_dir = os.path.dirname(os.path.abspath(__file__))
        executable = os.path.abspath(os.path.join(current_dir, 'grarep_exe/grarepimp/src/main.py'))
        tempGraphPath = os.path.abspath(os.path.join(current_dir, 'grarep_exe/tempGraph/tempGraph.csv'))
        outputPath = os.path.abspath(os.path.join(current_dir, 'grarep_exe/tempGraph/tempOutput.csv'))
        
        with open(source_graph, 'r') as source, open(tempGraphPath, 'w') as tempGraph:
            tempGraph.write('id1,id2\n')
            for line in source:
                tempGraph.write(','.join(line.split(' ')))
        
        args = []
        args.append('python')
        args.append(executable)
        args.append("--edge-path " + tempGraphPath)
        args.append("--output-path " + outputPath)
        args.append("--dimensions %d" % dim)
        args.append("--order %d" % order)
        args.append("--iterations %d" % iterations)
        args.append("--seed %d" % seed)
        print(args)
        
        call(args)
        
        
        
        
if __name__ == '__main__':
    grarep = GraRep()
    grarep.calculate_layout(source_graph=sys.argv[1])