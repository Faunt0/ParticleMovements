import math
import matplotlib.pyplot as plt
#from matplotlib.animation import FuncAnimation, PillowWriter
import numpy as np
import matplotlib.animation as animation
from decimal import *

#constants
G = 6.67 * 10**-11
# defining a certain radius of where to look for different particles to interact with
# to be implemented
#r = 2



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
    elif dx == 0 and dy > 0:
        #when its directly below the mass particle
        corner = 90
    elif dy == 0 and dx < 0:
        #when its directly right to the mass particle
        corner = 180
    elif dy == 0 and dx > 0:
        #when its directly to the left of the mass particle
        corner = 0

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
        self.xcoords = [self.sv[0]]
        self.ycoords = [self.sv[1]]
    def position(self, t):
        mvA = vectorMultiply(self.mv, t)

        return vectorsAdd(vectorMultiply(self.mv, t), self.sv)
    def vectorLength(self):
        veclen = 0
        for i in self.mv:
            veclen += math.pow(i, 2)
        
        return math.sqrt(veclen)

# The Inter Particle Force Calculator, at your service!
def IPFC (p1, mp2, t):
    r = 0
    for i in range(0, len(p1.position(t))):
        r += (p1.position(t)[i] - mp2.position(t)[i])**2
   

    f = G * (p1.mass * mp2.mass) / r
    fx = math.cos(math.radians(vectorsCorner(p1, mp2, t))) * f
    fy = math.sin(math.radians(vectorsCorner(p1, mp2, t))) * f
    return [f, fx, fy]


# Moving Particles
p1 = Particle([-5,-9], [1.70,-0.7], 80000)
#p1 = Particle([-1,0], [-1.15,2.0], 80000)
orbitalParticles = [p1]

# Mass particles
p2 = Particle([10,10], [0,0], 10050000)
p3 = Particle([100,100], [0,0], 1000000)
#p4 = Particle([50,-90], [0,0], 20000000)

massParticles = [
        Particle([10,10], [0,0], 10050000), 
        Particle([100,100], [0,0], 900000),
        #p4,
    ]
#massParticles = [p2]



# The rendering of the points and trails. before this all the forces being applied should be calculated


pitch = 0.0001
nstep = round(1/pitch)
for t in range(0, 1):
    stepPitch = t
    for step in range(0, nstep):
        force = [0,0]
        for mp in massParticles:
            force = vectorsAdd(force, [IPFC(p1, mp, stepPitch)[1], IPFC(p1, mp, stepPitch)[2]])
        #newPos = vectorsAdd(p1.sv, p1.mv, [force[1], force[2]])
        newPos = vectorsAdd(p1.sv, p1.mv, [force[0], force[1]])
        p1.sv = newPos
        #p1.mv = vectorsAdd(p1.mv, [force[1], force[2]])
        p1.mv = vectorsAdd(p1.mv, [force[0], force[1]])
        
        p1.xcoords.append(float(newPos[0]))
        p1.ycoords.append(float(newPos[1]))

        stepPitch += pitch
#        print(f'step = {step}\tnewPos1: {newPos}\tforce = {force[0]}\tfx = {force[1]}\tfy = {force[2]}')

fig, ax = plt.subplots()
x, y = [], []
line, = ax.plot(p1.xcoords, p1.ycoords, 'm.')
massPoints = [ax.plot(mp.sv[0], mp.sv[1], 'rx') for mp in massParticles]

#animation proces
def init():
    ax.set_xlim(-100, 110)
    ax.set_ylim(-70, 125)
    return line, massPoints,

def update(frame):
    x.append(p1.xcoords[frame])
    y.append(p1.ycoords[frame])
    line.set_data(x, y)
    return line,

def animate(save=False):
    ani = animation.FuncAnimation(fig, update, len(p1.xcoords), init_func=init, interval=20, blit=True, save_count=50)
    if save == True:
        ani.save('animgif5.gif')

#animate()

#plt.plot(p1.xcoords, p1.ycoords, label="particle movement")
#plt.plot([p2.sv[0]], [p2.sv[1]], 'ro' )
#plt.legend()
plt.show()
