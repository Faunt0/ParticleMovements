import math
import matplotlib.pyplot as plt
import numpy as np
from decimal import *

#constants
G = 6.67 * 10**-11
# defining a certain radius of where to look for different particles to interact with
r = 2


def vectorsAdd(vector1, vector2):
    newVector = []
    for i in range(0, len(vector1)):
        newVector.append(float(Decimal(vector1[i]) + Decimal(vector2[i])))
    print(f'newVector: {newVector}')
    return newVector


#def vectorsAdd(*vectors):
#    newVector = list(vectors)[0] 
#    for i in range(1, len(list(vectors))):
#        for j in range(0, len(newVector)):
#            newVector[j] = Decimal(newVector[j]) + Decimal(list(vectors)[i][j])
#   
#    return newVector




def vectorMultiply(vector, l):
    newVector = []
    for i in vector:
        newVector.append(i * l)
    return newVector

def vectorsCorner(v1, v2, t):
    # this is for 2 dimensions however
    """ need to add a way to locate the other point precisely
    to get the right direction of forces. this will be difficult."""
    
    dx = v2.position(t)[0] - v1.position(t)[0]
    dy = v2.position(t)[1] - v1.position(t)[1]
   
    if dx == 0 and dy == 0:
        print('this is when they both collide!')
        corner = 0 #this shouldn't be 0
    elif dx == 0 and dy < 0:
        #when its directly above the mass particle
        corner = -90
    elif dx == 0 and dy > 0:
        #when its directly below the mass particle
        corner = 90
    elif dy == 0 and dx < 0:
        #when its directly right to the mass particle
        corner = 0
    elif dy == 0 and dx > 0:
        #when its directly to the left of the mass particle
        corner = 180

    elif dx < 0 and dy < 0:
        #when the particle is in Q1 of the mass particle, top right
        corner = -90 - math.degrees(math.atan(dy / dx))
    elif dx < 0 and dy > 0:
        #when the particle is in Q2, bottom right
        corner = math.degrees(math.atan(dy / dx)) - 180
    elif dx > 0 and dy < 0:
        #particle is in top left to the mass particle
        corner = math.degrees(math.atan(dy / dx))
    else:
        """if both are positive the movable particle
        is closer to the origin """
        corner = math.degrees(math.atan(dy / dx))
   
        corner = math.degrees(math.atan(dy / dx))
    return corner

class Particle:
    def __init__(self, sv, mv, mass):
        self.sv = sv
        self.mv = mv
        self.mass = mass
    def position(self, t):
        mvA = vectorMultiply(self.mv, t)

#        return vectorsAdd(self.sv, mvA)
        return vectorsAdd(mvA, self.sv)
    def vectorLength(self):
        veclen = 0
        for i in self.mv:
            veclen += math.pow(i, 2)
        
        return math.sqrt(veclen)



#p1 = Particle([1,1], [1,1], 2)
p1 = Particle([-1,0], [5.0,0.0], 800)
p2 = Particle([5,5], [0,0], 900000000)
p3 = Particle([-2,5], [0,0], 10000000)
#print(p1.position(2))
#print(vectorMultiply(p1.mv, 2))
print(vectorsCorner(p1, p2, 0))

# The Inter Particle Force Calculator, at your service!
def IPFC (p1, p2, t):
    r = 0
    for i in range(0, len(p1.position(t))):
        r += (p1.position(t)[i] - p2.position(t)[i])**2
   

    #f = G * (p1.mass * p2.mass) / r
    f = format(Decimal(G * (p1.mass * p2.mass)) / Decimal(r), '.2E')
    fx = format(Decimal(math.cos(math.radians(vectorsCorner(p1, p2, t)))) * Decimal(f), '.2E')
    fy = format(Decimal(math.sin(math.radians(vectorsCorner(p1, p2, t)))) * Decimal(f), '.2E')
    return [f, fx, fy]

xcoords = []
ycoords = []

plt.plot([p1.sv[0]], [p1.sv[1]], 'bo' )
print(f'p1: {p1.sv}\tp2: {p2.sv}')
pitch = 0.005
nstep = round(1/pitch)
for t in range(0, 1):
    #newPos = p1.position(t)
    stepPitch = t
    for step in range(0, nstep):
        
        force = IPFC(p1, p2, stepPitch)
        newPos = vectorsAdd(p1.position(stepPitch), [force[1], force[2]])
        p1.sv = newPos
        newPos[0] = format(newPos[0], '.6E')
        newPos[1] = format(newPos[1], '.6E')
        xcoords.append(float(newPos[0]))
        ycoords.append(float(newPos[1]))

        print(f'step = {step}\tnewPos1: {newPos}\tforce = {force[0]}\tfx = {force[1]}\tfy = {force[2]}')
        stepPitch += pitch


#print(vectorsCorner(p1, p2, 0))
#fig, ax = plt.subplots()
#ax.plot(xcoords, ycoords, label="particle movement")
#ax.plot([p2.sv[0]], [p2.sv[1]], label="Big mass")
#ax.legend()
#ax.title("particle movements")

plt.plot(xcoords, ycoords, label="particle movement")
plt.plot([p2.sv[0]], [p2.sv[1]], 'ro' )
plt.legend()
plt.title("particle movements")
plt.show()
