import sys
import os
from pathlib import Path
import csv
from time import time

from embedding.spring import Spring
from embedding.kamada_kawai import KamadaKawai
from embedding.hope import Hope
from embedding.lap_eig import LapEig
from embedding.loc_lin_emb import LocLinEmb

def getFiles(path):
    result = []

    if os.path.isfile(path): return result.append(path)

    for filename in os.listdir(path):
        f = os.path.join(path, filename)
        if os.path.isfile(f): result.append(f)
        else:
            result.extend(getFiles(f))
    
    return result

def saveNodeListAsCSV(savepath, layout):
    Path(savepath).parent.mkdir(exist_ok=True, parents=True)
    
    with open(savepath, 'w', newline='') as file:
        writer = csv.writer(file)
        for value in layout:
            writer.writerow(value)

        
def main(argv):
    """
    Expects 2 args:
    1- Data type of the input data -> -edl: Edge List
    2- Relative or real path name of the input data or the directory of the input data
    """

    if len(argv) != 2:
        raise ValueError(print(main.__doc__))
    sourcepath = os.path.realpath(argv[1])
    
    embeddings = list()
    embeddings.append(Spring())
    embeddings.append(KamadaKawai())
    embeddings.append(Hope())
    embeddings.append(LapEig())
    embeddings.append(LocLinEmb())
    
    if argv[0] == '-edl':
        for sourcepath in getFiles(argv[1]):
            for embedding in embeddings:
                savepath = os.path.join('result', embedding._name, sourcepath + ".csv")
                t0 = time()
                layout = embedding.calculate_layout(sourcepath)
                saveNodeListAsCSV(savepath, layout)
                
                

if __name__ == "__main__":
    main(sys.argv[1:])