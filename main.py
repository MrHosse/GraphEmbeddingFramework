import sys
import os
import run

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
    embeddings.append('kamada_kawai')
    embeddings.append('hope')
    embeddings.append('node2vec')
    embeddings.append('struc2vec')
    
    run.group('embed')
    
    run.add(
        "calculating embedding",
        "python embedding/[[embedding]].py [[edgelist]]",
        {'embedding': embeddings,
        'edgelist': getFiles('input_data')},
        allowed_return_codes=[0,124],
    )
    
    evaluations = list()
    evaluations.append('basic_link_prediction')
    
    run.add(
        "evaluating",
        "python evaluation/[[evaluation]].py [[edgelist]] embedding_result/[[embedding]]/[[edgelist]]",
        {'evaluation': evaluations,
         'embedding': embeddings,
         'edgelist': getFiles('input_data')},
    )

    run.run()
    