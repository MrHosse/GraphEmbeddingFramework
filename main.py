import os
import run
import shutil
from subprocess import call, DEVNULL

def getFiles(path) -> list:
    result = []
    
    if os.path.isfile(path) and path.split('/')[-1] != 'README.md': return result.append(path)
    elif os.path.isdir(path):
        for filename in os.listdir(path):
            f = os.path.join(path, filename)
            if os.path.isfile(f) and filename != 'README.md': 
                result.append(f)
            elif os.path.isdir(f) and filename != 'README.md':
                result.extend(getFiles(f))
    
    return result

if __name__ == "__main__":

    if os.path.exists('embedding/verse_exe/temp'):
        shutil.rmtree('embedding/verse_exe/temp')
    if os.path.exists('embedding/struc2vec_exe/temp'):
        shutil.rmtree('embedding/struc2vec_exe/temp')
    
    embeddings = list()
    embeddings.append('spring')
    embeddings.append('kamada_kawai')
    embeddings.append('node2vec')
    embeddings.append('struc2vec')
    embeddings.append('verse')
    
    run.group('embed')
    
    run.add(
        "layout",
        "python embedding/[[embedding]].py [[edgelist]]",
        {'embedding': embeddings,
        'edgelist': getFiles('input_data')},
        stdout_file='embedding_result/[[embedding]]/[[edgelist]]'
    )
    
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
    run.add(
        "evaluate",
        "python evaluation/[[evaluation]].py [[edgelist]] " + ' '.join(similarity_metric),
        {'evaluation': evaluations,
        'edgelist': getFiles('input_data')},
        stdout_file='evaluation_result/[[edgelist]]/[[evaluation]].csv',
    )

    run.run()