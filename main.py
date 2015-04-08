import sys, os
import math
import random as rn
from numpy import random, array

class nodes_neighbors(object):
    def __init__(self, m, n):
        #--setting the initial values and the center node
        self.x = m
        self.y = n
        self.nodes = {}
        #--set the center node only if m,n == odd integers
        if self.x % 2 == 0:
            self.center_node = None
        else:
            self.center_node = (m/2, n/2)

        #--assign random weights to each node
        self.n = xrange(n)
        for i in self.n:
            for j in xrange(0, n):
                quadrant = 0
                coordinates = (i, j)
                self.nodes[coordinates] = random.random((1, m))[0]

        #--keep the list of keys or node coordinates separately
        self.keys  = self.nodes.keys()
        #--set the progress tracking metrics
        self.set_xy()
    
    def set_xy(self):
        self.n_done = {}
        self.x_done = []
        self.y_done = []
        self.x_coords = list(set(map(lambda n: n[0], self.keys)))
        self.y_coords = list(set(map(lambda n: n[1], self.keys)))
    
    def reducer(self, n, coords):
        #--if the given radius is already passed, then dont bother to do all the calculations again
        if self.n_done.has_key(n):
            return self.n_done[n]
        else:
            #--if the passed node is a center node
            if coords == self.center_node:
                if n == int((self.x-1)/2):
                    self.n_done[n] = self.keys
                    return self.n_done[n]

                #--finding the most distant column and row from the given coordinate
                d_xs = [max(self.x_coords), min(self.x_coords)]
                d_ys = [max(self.y_coords), min(self.y_coords)]
                
                for i, j in zip(d_xs, d_ys):
                    self.x_done.append(i)
                    self.y_done.append(j)
                    if i in self.x_coords:
                        del self.x_coords[self.x_coords.index(i)]
                    if j in self.y_coords:
                        del self.y_coords[self.y_coords.index(j)]
                
                self.allowed = filter(lambda p: p[0] not in self.x_done and p[1] not in self.y_done, self.keys)

                self.n_done[n] = self.allowed
                return self.n_done[n]
            else:
                #--if radius == n - 1 then return all the nodes, because you know its the beginning
                if n == self.x - 1:
                    self.n_done[n] = self.keys
                    return self.n_done[n]
                else:
                    #--get the x, y points
                    x, y = coords
                    
                    #--finding the most distant column and row from the given coordinate
                    d_x = max(self.x_coords, key = lambda j: abs(j-x))
                    d_y = max(self.y_coords, key = lambda j: abs(j-y))

                    #--keeping track of what rows and columns are done
                    self.x_done.append(d_x)
                    self.y_done.append(d_y)

                    #--additionally, deleting the done rows and columns from their temp list
                    del self.x_coords[self.x_coords.index(d_x)]
                    del self.y_coords[self.y_coords.index(d_y)]
                    
                    self.allowed = filter(lambda p: p[0] not in self.x_done and p[1] not in self.y_done, self.keys)
                    
                    self.n_done[n] = self.allowed
                    return self.n_done[n]

    def simulate(self):
        keys = self.keys
        key = rn.sample(keys, 1)[0]
        
        if key == self.center_node:
            init = int((self.x-1)/2)
        else:
            init = self.x-1
        
        for j in range(init, -1, -1):
            for i in range(10):
                t = self.reducer(j, key)
                print sorted(t), key
                print "@@@@"
        
        

if __name__ == '__main__':
    m  = raw_input("enter the value for m: ")
    n = raw_input("enter the value for n: ")
    if int(n) and int(m) and n == m:
        obj = nodes_neighbors(int(m), int(n))
        obj.simulate()
    else:
        print "please check the provided values..terminating."
