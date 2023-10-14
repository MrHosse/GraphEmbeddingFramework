import sys
import os
from subprocess import call, DEVNULL
import argparse
import json
import time
import run

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from abstract_embedder import AbstractEmbedder
sys.path.append(os.path.dirname(__file__))
from verse_exe.python.embedding import Embedding
    
class Verse(AbstractEmbedder):

    def __init__(self):
        self._name = 'verse'
        self._filename = 'embedding/verse.py'
        self._embpath = 'embedding_result/verse/'
        self._evlpath = 'evaluation_result/'
    
    def create_run(inputs):
        with open('embedding/verse/config.json', 'r') as config_file:
            config = json.load(config_file)
        
        # list of integers
        dim_list = config['dim'] or ['default']
        dim_list = [' -d ' + str(dim) if (dim != 'default') else '' for dim in dim_list]
        
        # list of floats
        alpha_list = config['alpha'] or ['default']
        alpha_list = [' -a ' + str(alpha) if (alpha != 'default') else '' for alpha in alpha_list]
        
        # list of integers
        threads_list = config['threads'] or ['default']
        threads_list = [' -t ' + str(threads) if (threads != 'default') else '' for threads in threads_list]
        
        # list of integers
        nsamples_list = config['nsamples'] or ['default']
        nsamples_list = [' -ns ' + str(nsamples) if (nsamples != 'default') else '' for nsamples in nsamples_list]
        
        # list of integers
        steps_list = config['steps'] or ['default']
        steps_list = [' -e ' + str(steps) if (steps != 'default') else '' for steps in steps_list]
        
        # list of floats
        global_lr_list = config['global_lr'] or ['default']
        global_lr_list = [' -lr ' + str(global_lr) if (global_lr != 'default') else '' for global_lr in global_lr_list]
        
        run.add(
            'layout verse',
            "python embedding/verse/verse.py -src [[edgelist]][[dim]][[alpha]][[threads]][[nsamples]][[steps]][[global_lr]]",
            {
             'edgelist': inputs,
             'dim': dim_list,
             'alpha': alpha_list,
             'threads': threads_list,
             'nsamples': nsamples_list,
             'steps': steps_list,
             'global_lr': global_lr_list},
            stdout_file='embedding_result/verse/[[edgelist]][[dim]][[alpha]][[threads]][[nsamples]][[steps]][[global_lr]]'
        )
    
    def calculate_layout(self, 
                         source_graph, 
                         dim=128, 
                         alpha=0.85,
                         threads=4,
                         nsamples=3,
                         steps=100000,
                         global_lr=0.0025):
        
        cwd = f'embedding/verse/verse_exe/temp/{source_graph}-d{dim}-a{alpha}-t{threads}-ns{nsamples}-e{steps}-lr{global_lr}'
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
        args.append("-steps %d" % steps)
        args.append("-lr " + str(global_lr))
        
        call(' '.join(args), stdout=DEVNULL, shell=True, cwd=cwd)
        
        embedding = Embedding(cwd + '/' + tempgraph_path, dim, mapping_path)
        os.makedirs(self._embpath + '/'.join(source_graph.split('/')[:-1]), exist_ok=True)
        
        output = ''
        for node in mapping.keys():
            output += (node + ',' + ','.join(list(map(str, embedding[node]))) + '\n')

        return output
 
if __name__ == '__main__':
    verse = Verse()
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-src", "--source_graph", help="path to the edgelist" , type=str)
    parser.add_argument("-d", "--dim", help="Number of dimensions", type=int, default=128)
    parser.add_argument("-a", "--alpha", help="value for ppr alpha", type=float, default=0.85)
    parser.add_argument("-t", "--threads", help="the number of parallel threads", type=int, default=4)
    parser.add_argument("-ns", "--nsamples", help="number of negativ samples", type=int, default=3)
    parser.add_argument("-e", "--steps", help="number of steps (epochs)", type=int, default=100000)
    parser.add_argument("-lr", "--global_lr", help="global level relation", type=float, default=0.0025)
    
    args = parser.parse_args()
    source_graph = args.source_graph
    dim = args.dim
    alpha = args.alpha
    threads = args.threads
    nsamples = args.nsamples
    steps = args.steps
    global_lr = args.global_lr
    
    t0 = time.time()
    result = verse.calculate_layout(source_graph=source_graph,
                                    dim=dim,
                                    alpha=alpha,
                                    threads=threads,
                                    nsamples=nsamples,
                                    steps=steps,
                                    global_lr=global_lr)
    t1 = time.time()
    
    print(source_graph + ' ' + str(t1 - t0))
    print(result)