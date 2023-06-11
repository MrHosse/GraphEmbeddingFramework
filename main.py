import sys
import os
from spring import spring
from kamada_kawai import kamada_kawai

def getFiles(path):
    result = []

    if os.path.isfile(path): return result.append(path)

    for filename in os.listdir(path):
        f = os.path.join(path, filename)
        if os.path.isfile(f): result.append(f)
        else:
            result.extend(getFiles(f))
    
    return result


def main(argv):
    """
    Expects 2 args:
    1- Data type of the input data -> -edl: Edge List
    2- Relative or real path name of the input data or the directory of the input data
    """

    if len(argv) != 2:
        raise ValueError(print(main.__doc__))

    sourcepath = os.path.realpath(argv[1])

    if argv[0] == '-edl':
        for sourcepath in getFiles(argv[1]):
            spring.draw(sourcepath, os.path.realpath('result'), sourcepath)
            kamada_kawai.draw(sourcepath, os.path.realpath('result'), sourcepath)


if __name__ == "__main__":
    main(sys.argv[1:])