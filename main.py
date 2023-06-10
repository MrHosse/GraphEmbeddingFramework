import sys
import os
from spring import spring

def main(argv):
    """
    Expects 2 args:
    1- Data type of the input data -> -edl: Edge List
    2- Relative or real path name of the input data
    """

    if len(argv) != 2:
        raise ValueError(print(main.__doc__))

    sourcepath = os.path.realpath(argv[1])

    if argv[0] == '-edl':
        spring.draw(sourcepath, os.path.realpath('result'), argv[1])


if __name__ == "__main__":
    main(sys.argv[1:])