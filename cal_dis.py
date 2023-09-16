import math

points = [[-0.21034531729842504,-1.0],
          [-0.1660577067858938,-0.7773489203976495],
          [0.08110010822887385,0.9087658545008273],
          [0.29530291585544494,0.8685830658968222]]

s = ''
for i in range(len(points)):
    for j in range(len(points)):
        if j > i:
            s += str(i) + ',' + str(j) + ': ' + str(math.dist(points[i], points[j])) + '\n'

with open('test_result', 'w') as f:
    f.write(s)
