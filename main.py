import sys
import os
import run
import shutil

def getFiles(path):
    result = []

    if os.path.isfile(path): return result.append(path)

    for filename in os.listdir(path):
        f = os.path.join(path, filename)
        if os.path.isfile(f): result.append(f)
        else:
            result.extend(getFiles(f))
    
    return result

if __name__ == "__main__":
    
    embeddings = list()
    embeddings.append('spring')
    #embeddings.append('kamada_kawai')
    #embeddings.append('hope')
    embeddings.append('node2vec')
    embeddings.append('struc2vec')
    embeddings.append('verse')
    
    run.group('embed')
    
    os.makedirs('embedding_result', exist_ok=True)
    
    run.add(
        "calculating embedding",
        "python embedding/[[embedding]].py [[edgelist]]",
        {'embedding': embeddings,
        'edgelist': getFiles('input_data')},
        allowed_return_codes=[0,124],
    )
    
    evaluations = list()
    evaluations.append('average_error_link_prediction')
    evaluations.append('precision_at_k_link_prediction')
    
    if os.path.exists('evaluation_result'):
        shutil.rmtree('evaluation_result')
    os.makedirs('evaluation_result', exist_ok=True)
    
    run.add(
        "evaluating",
        "python evaluation/[[evaluation]].py [[edgelist]] embedding_result/[[embedding]]/[[edgelist]]",
        {'evaluation': evaluations,
         'embedding': embeddings,
         'edgelist': getFiles('input_data')},
    )

    run.run()
    