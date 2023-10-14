import os
import run
from embedding.spring.spring import Spring
from embedding.kamada_kawai.kamada_kawai import KamadaKawai
from embedding.node2vec.node2vec import Node2Vec
from embedding.struc2vec.struc2vec import Struc2Vec
from embedding.verse.verse import Verse

def getFiles(pathList) -> list:
    result = []
    
    for path in pathList:
        result.extend(getFilesFromPath(path))
        
    return result

def getFilesFromPath(path) -> list:
    result = []
    
    if os.path.isfile(path) and path.split('/')[-1] != 'README.md': return result.append(path)
    elif os.path.isdir(path):
        for filename in os.listdir(path):
            f = os.path.join(path, filename)
            if os.path.isfile(f) and filename != 'README.md': 
                result.append(f)
            elif os.path.isdir(f) and filename != 'README.md':
                result.extend(getFilesFromPath(f))
    
    return result

if __name__ == "__main__":
    
    input = list()
    input.append('input_data')

    """ if os.path.exists('embedding/verse_exe/temp'):
        shutil.rmtree('embedding/verse_exe/temp')
    if os.path.exists('embedding/struc2vec_exe/temp'):
        shutil.rmtree('embedding/struc2vec_exe/temp') """
    
    embeddings = list()
    embeddings.append(Spring)
    embeddings.append(KamadaKawai)
    embeddings.append(Node2Vec)
    embeddings.append(Struc2Vec)
    embeddings.append(Verse)
    
    run.group('layout')
    for embedding in embeddings:
        embedding.create_run(getFiles(input))
    
    evaluations = list()
    evaluations.append('average_error_link_prediction')
    evaluations.append('precision_at_k_link_prediction')

    # embedding#similarity_metric
    similarity_metric = list()
    similarity_metric.append('spring#EuclidianDistance')
    similarity_metric.append('kamada_kawai#EuclidianDistance')
    similarity_metric.append('node2vec#EuclidianDistance')
    similarity_metric.append('struc2vec#EuclidianDistance')
    similarity_metric.append('verse#EuclidianDistance')

    os.makedirs('evaluation_result', exist_ok=True)
    run.group('evaluation')
    run.add(
        "evaluate",
        "python evaluation/[[evaluation]].py [[edgelist]] " + ' '.join(similarity_metric),
        {'evaluation': evaluations,
        'edgelist': getFiles(input)},
        stdout_file='evaluation_result/[[edgelist]]/[[evaluation]].csv',
    )

    run.run()