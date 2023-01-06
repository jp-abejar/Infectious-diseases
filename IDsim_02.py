#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 11 11:25:59 2022

@author: jabejar
"""


import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from collections import Counter

# define the number of people and the size of the grid
class idSimulation():
    def __init__(self, N = 500 , width = 100, height = 1000, infection_rate = 0.05, recovery_rate = 0.1, infProb = 0.8, inf_radius = 4,log = False, fi = './StatusLog.txt'):
        self.N = N
        self.width = width
        self.height = height
        
        # initialize the positions of the people on the grid
        self.positions = np.random.randint(0, width, size=(N, 2))
        
        # initialize the health status of each person (0 = healthy, 1 = infected, 2 = recovered)
        self.status = np.zeros(N)
        
        # set the initial infection rate and recovery rate
        self.infection_rate = infection_rate
        self.recovery_rate =recovery_rate
        
        self.infProb = infProb # probability to infect when within the radius
        
        self.inf_radius = inf_radius # radius of infection
        # set the initial number of infected people
        num_infected = int(N * infection_rate)
        self.status[:num_infected] = 1
        
        # initialize the figure and axes for the animation
        self.fig, self.ax = plt.subplots()
        self.fig2, self.ax2 = plt.subplots()
        
        # initialize the scatter plot for the people on the grid
        self.scatter = self.ax.scatter(self.positions[:, 0], self.positions[:, 1], c=self.status, cmap='brg')
        self.log = log
        
        if log:
            self.statusLists = []
            self.fi = fi
        
        ''' 
        0   : succeptible, 
        0.35: recovered, 
        0.5: removed,
        1.0: infected, 
             
             
             '''
        self.stats = [0,0.35,0.5,1]
        self.statInd = ['succeptible','recovered','removed','infected']
        self.col = 'byrg'
        
        # show the animation
        plt.show()
        
        
        
        
    def graphUpdate(self,frame):
        
        
        cnts = Counter(self.status)
        print(cnts)
        # ax2.cla()
        for i,stat in enumerate(self.stats):
            self.ax2.plot(frame,cnts[stat],self.col[i]+'.',label = self.statInd[i])
        
        
    def grphInit(self):
        
        
        cnts = Counter(self.status)
        self.ax2.cla()
        for i,stat in enumerate(self.stats):
            self.ax2.plot(0,cnts[stat],self.col[i]+'.',label = self.statInd[i])
        self.ax2.legend()
        
        
        
        
        
    # define the update function for the animation
    def update(self,frame):
       
        
        # update the health status of each person
        # print(status)
        for i in range(self.N):
            # if the person is healthy, check if they have been infected
            if self.status[i] == 0:
                # compute the distance to each infected person
                dist = np.sqrt(np.sum((self.positions[i] - self.positions[self.status == 1])**2, axis=1))
    
                # if the person is within the infection radius, they become infected
                if np.any(dist <= self.inf_radius):
                    if np.random.rand() < self.infProb:
                        self.status[i] = 1
    
            # if the person is infected, check if they have recovered
            elif self.status[i] == 1:
                if np.random.rand() > 0.8:
                    if np.random.rand() < self.recovery_rate:
                        self.status[i] = 0.35
                    else:
                        self.status[i] = 0.5
        
        # update the positions of each person
        for i in range(self.N):
            # if the person is healthy or recovered, they move randomly
            if self.status[i] != 0.5:
                self.positions[i] += np.random.randint(-1, 2, size=2)
        
                # make sure the positions are within the bounds of the grid
                self.positions[i] = np.clip(self.positions[i], 0, self.width-1)
    
        # update the scatter plot with the new positions and health status
        self.scatter.set_offsets(self.positions)
        self.scatter.set_array(self.status)
        if self.log:
            self.statusLists.append(self.status)
            
            if frame == 1000:
                np.save(self.fi,np.array(self.statusLists))
                self.log = False

# create the animation using the update function

if __name__ == "__main__":
    
    sim1 = idSimulation()
    anim = animation.FuncAnimation(sim1.fig, sim1.update, frames=1000, interval=100)
    anim2 = animation.FuncAnimation(sim1.fig2, sim1.graphUpdate, frames=1000, interval=100,init_func = sim1.grphInit)
    
