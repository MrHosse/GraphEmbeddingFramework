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

    run.add(
        "embed",
        "timeout 20 python embedding/[[embedding]].py [[input]]",
        {'embedding': embeddings,
        'input': getFiles('input_data')},
        stdout_file="result/[[embedding]]/[[input]].txt",
        stdout_res=lambda args: (
            "[[stdout]]" if args['stdout'] != "" else "Calculation wasn't successful."
        ),
        allowed_return_codes=[0, 1, 124],
    )

    run.run()
     
    