from decimal import *

def vectorsAdd(*vectors):
    newVector = list(vectors)[0]
    for i in range(1, len(vectors)):
        for j in range(0, len(newVector)):
            newVector[j] = Decimal(newVector[j]) + Decimal(list(vectors)[i][j])

    return newVector


va = vectorsAdd([1, 2], [4, 10])

print(float(va[0]), float(va[1]))
