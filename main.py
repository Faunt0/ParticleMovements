import math
import matplotlib.pyplot as plt
import numpy as np
from decimal import *

#constants
G = 6.67 * 10**-11
# defining a certain radius of where to look for different particles to interact with
r = 2



def vectorsAdd(*vectors):
    newVector = list(vectors)[0] 
    for i in range(1, len(list(vectors))):
        for j in range(0, len(newVector)):
            newVector[j] = newVector[j] + list(vectors)[i][j]
   
    return newVector




def vectorMultiply(vector, l):
    newVector = []
    for i in vector:
        newVector.append(i * l)
    return newVector

def vectorsCorner(v1, v2, t):
    # this is for 2 dimensions however
    """ need to add a way to locate the other point precisely
    to get the right direction of forces. this will be difficult."""
    #think I found a way, 'ave a look    
    dx = v2.position(t)[0] - v1.position(t)[0]
    dy = v2.position(t)[1] - v1.position(t)[1]
    corner = 0   
    if dx == 0 and dy == 0:
        print('this is when they both collide!')
        corner = 0 #this shouldn't be 0
    elif dx == 0 and dy < 0:
        #when its directly above the mass particle
        corner = 90
#        corner = 0
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

    return corner

class Particle:
    def __init__(self, sv, mv, mass):
        self.sv = sv
        self.mv = mv
        self.mass = mass
    def position(self, t):
        mvA = vectorMultiply(self.mv, t)

        return vectorsAdd(vectorMultiply(self.mv, t), self.sv)
    def vectorLength(self):
        veclen = 0
        for i in self.mv:
            veclen += math.pow(i, 2)
        
        return math.sqrt(veclen)



p1 = Particle([-1,0], [0.9,-2.0], 80000)
p2 = Particle([10,10], [0,0], 9000000)
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
    f = G * (p1.mass * p2.mass) / r
    fx = math.cos(math.radians(vectorsCorner(p1, p2, t))) * f
    fy = math.sin(math.radians(vectorsCorner(p1, p2, t))) * f
    return [f, fx, fy]

xcoords = []
ycoords = []

plt.plot([p1.sv[0]], [p1.sv[1]], 'bo' )
print(f'p1: {p1.sv}\tp2: {p2.sv}')
pitch = 0.001
nstep = round(1/pitch)
for t in range(0, 1):
    #newPos = p1.position(t)
    stepPitch = t
    for step in range(0, nstep):
        
        force = IPFC(p1, p2, stepPitch)
        #newPos = vectorsAdd(p1.position(stepPitch), [force[1], force[2]])
        newPos = vectorsAdd(p1.sv, p1.mv, [force[1], force[2]])
        p1.sv = newPos
        p1.mv = vectorsAdd(p1.mv, [force[1], force[2]])
        
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
# just for the ease of mind, I remove the last value since it seems to fuck up often around there.
#xcoords[len(xcoords)-1] = 0
#ycoords[len(ycoords)-1] = 0

plt.plot(xcoords, ycoords, label="particle movement")
plt.plot([p2.sv[0]], [p2.sv[1]], 'ro' )
plt.legend()
plt.title("particle movements")
plt.show()
