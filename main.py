import math
import random
import matplotlib.pyplot as plt
#from matplotlib.animation import FuncAnimation, PillowWriter
import numpy as np
import matplotlib.animation as animation
from decimal import *

#constants
G = 6.67 * 10**-11
c = 299792458
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
    def __init__(self, sv, mv, mass, ismp):
        self.sv = sv
        self.mv = mv
        self.mass = mass
        self.xcoords = [self.sv[0]]
        self.ycoords = [self.sv[1]]
        self.rs = (2 * G * self.mass) / (c**2)
        self.rs = 30
        self.ismp = False
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
  
    #doesn't work properly
    if math.sqrt(r) < mp2.rs:
#       print('the particle will be sucked in ;')
        #p1.sv = mp2.sv
        #p1.mv = [0, 0]
        del p1
        return [0,0,0]
    else:
        f = G * (p1.mass * mp2.mass) / r
        fx = math.cos(math.radians(vectorsCorner(p1, mp2, t))) * f
        fy = math.sin(math.radians(vectorsCorner(p1, mp2, t))) * f
#    else:
#        f = G * (p1.mass * mp2.mass) / r
#        fx = math.cos(math.radians(vectorsCorner(p1, mp2, t))) * f
#        fy = math.sin(math.radians(vectorsCorner(p1, mp2, t))) * f
        return [f, fx, fy]

def particleMoves(p):
    nstep = round(1/pitch)
    for t in range(0, grandPitch):
        stepPitch = t
        for step in range(0, nstep):
            force = [0,0]
            for mp in massParticles:
                force = vectorsAdd(force, [IPFC(p, mp, stepPitch)[1], IPFC(p, mp, stepPitch)[2]])
            #newPos = vectorsAdd(p1.sv, p1.mv, [force[1], force[2]])
            newPos = vectorsAdd(p.sv, p.mv, [force[0], force[1]])
            p.sv = newPos
            #p1.mv = vectorsAdd(p1.mv, [force[1], force[2]])
            p.mv = vectorsAdd(p.mv, [force[0], force[1]])
            
            p.xcoords.append(float(newPos[0]))
            p.ycoords.append(float(newPos[1]))
    
            stepPitch += pitch
    #        print(f'step = {step}\tnewPos1: {newPos}\tforce = {force[0]}\tfx = {force[1]}\tfy = {force[2]}')

def init():
   #ax.set_xlim(-220, 200)
   #ax.set_ylim(-190, 250)
   #ax.set_xlim(-150, 250)
   #ax.set_ylim(-100, 200)

#   ax.set_xlim(-250, 375)
#   ax.set_ylim(-125, 160)

    ax.set_xlim(-320, 780)
    ax.set_ylim(-360, 775)
    
    ax.set_xlim(-1000, 780)
    ax.set_ylim(-500, 775)



#    ax.set_xlim(-50, 300)
#    ax.set_ylim(-100, 250)




    return lines, massPoints,

def update(frame, particles, lines):
    for line, p in zip(lines, particles):
        line.set_data(p.xcoords[0:frame], p.ycoords[0:frame])
    return lines

if __name__ == "__main__":
    print('calling main')
    
    # Moving Particles
    #p1 = Particle([-5,-9], [1.70,-0.7], 80000)
    #p1 = Particle([-1,0], [-1.15,2.0], 80000)
    orbitalParticles = [
        #Particle([10,90], [3.0,1.3], 800000, False),
        #Particle([-20,-13], [1.00,-3.7], 80000, False),
        Particle([150,-50], [-3.18,5.1], 80000, False),
        #Particle([-50,-100], [-2.1,-0.5], 840000, False),
        Particle([-100,-1], [-0.1,-0.1], 840000, False),
        Particle([-100,-1], [-2.1,-7.1], 840000, False),
        Particle([10,90], [-2.5,-0.1], 850000, False),
    ]
    #orbitalParticles = []
#    orbitalParticles = [Particle([random.randrange(-150, 150),random.randrange(-150, 150)], [random.randrange(-10, 10), random.randrange(-10, 10)], random.randint(800000, 1500000), False) for i in range(0, 50)]
    #orbitalParticles.append(Particle([150,150], [-1,-1], 166616))#between 80000-1000000))
    #orbitalParticles = [Particle([-70,-100-i*10], [1.5, -0.5], 800000) for i in range(0, 20)]
    #orbitalParticles = [Particle([70*math.cos(i),-600-80*math.sin(i)], [1.5, -0.5], 800000) for i in range(0, 20)]
    
    massParticles = [
        Particle([10,10], [0,0], 4050000, True), 
        Particle([150,100], [0,0], 10050000, True),
    #    Particle([-100,120], [0,0], 3600000),
    ]
    massParticles = [
    #    Particle([150,100], [0,0], 10050000, True),
    #    Particle([300,-400], [0,0], 10500000, True),
    #    Particle([-100,120], [0,0], 3600000, True),
    #    Particle([400,400], [0,0], 100500000, True),
#        Particle([-400,400], [0,0], 104500000, True),
        Particle([200,200], [0,0], 104500000, True),
        Particle([200,-200], [0,0], 104500000, True),
    ]
    
    
    grandPitch = 10
    pitch = 0.001
    for p in orbitalParticles:
        print(f'p: {orbitalParticles.index(p)}\tsv = {p.sv}\tmv = {p.mv}\tmass = {p.mass}')
        particleMoves(p)
    
    colors = 'bgcmyk' * 10
    colors = 'wgm' * 140
    fig, ax = plt.subplots()
    ax.set_facecolor('k')
    lines = [ax.plot(p.xcoords, p.ycoords, f'{colors[orbitalParticles.index(p)]}.')[0] for p in orbitalParticles]
    massPoints = [ax.plot(mp.sv[0], mp.sv[1], 'rx') for mp in massParticles]
    
    #animation proces
    #ani = animation.FuncAnimation(fig, update, round(grandPitch/pitch), fargs=(orbitalParticles, lines), init_func=init, interval=20, save_count=50)
    #ani.save('animgif9.gif')
    
    
    #plt.legend()
    plt.show()
    
    
