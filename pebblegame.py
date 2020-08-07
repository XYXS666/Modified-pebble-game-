'''
This is a modified pebble game algorithm written in python,translated from the origin 
https://github.com/coldlaugh/pebble-game-algorithm.
TO run this program, you need to have python.
By Xinyue Zhao, 2020/8/7
Reference Brian S. Smith, Magnus Egerstedt, and Ayanna Howard
Automatic Generation of Persistent Formations for Multi-Agent Networks Under Range Constraints
'''

import numpy as np

class pebble(object):

    def __init__(self):
        self.digraph = {} #directed graph
        self.graph = {} #undirected graph
        self.bond = [] #edges
        self.visited = [] #visit history
        self.agentcoor = {} #agnet coordinates --> 2D
        self.srange = 0 #sensing range 

    def clear(self):
        self.__init__()

    def eucldist(self,coords1,coords2):
        '''Calculates the euclidean distance between 2 lists of coordinates.'''
        coords1, coords2 = np.array(coords1),np.array(coords2)
        return np.sqrt(np.sum(coords1-coords2)**2)

    def calneighbor(self):
        '''Calculates the bonds connecting agents which have limited sensing range. '''
        if self.srange == 0:
            raise ValueError('sensing range must be greater than 0')
        coordinates = list(self.agentcoor.values())# coordinates is a list which contains all agent's coordinates.
        ''' double "for" calculates all inter-distance 
            and record the agents which have inter-distancs 
            smaller than sensing range.'''
        #print(list(coordinates))
        for i in range(0,len(coordinates)):   
            if i < len(coordinates)-1:
                for j in range(i+1,len(coordinates)):
                    distance = self.eucldist(coordinates[i],coordinates[j])
                    if distance <= self.srange: # etermine if inter-agent distance is smaller than sensing range
                        if i not in self.graph.keys():
                            self.graph[i] = [j]
                        else:    
                            self.graph[i].append(j) # record it in undirected graph.
                        if j not in self.graph.keys():
                            self.graph[j] = [i]
                        else:    
                            self.graph[j].append(i) # record it in undirected graph.
                        self.bond.append((i,j)) # all pairwise agents are contained in bond list.
    
    def add_bond(self, x, y):
        """
        :param x: a site
        :param y: a different site
        :return: if the new bond is independent: True, otherwise False.
        """
        # no self-loop bonds:
        if x == y:
            raise ValueError('add_bond must have two different sites')

        # smaller site first:
        x,y = sorted((x,y))

        # update directed graph
        sites = self.digraph.keys()
        if x not in sites:
            self.digraph[x] = [[y],1]
            if y not in sites:
                self.digraph[y] = [[],2]
            return True
        elif y not in sites:
            self.digraph[y] = [[x],1]
            return True
        elif self.collect_four_pebble(x,y):
            if y not in self.digraph[x][0]:
                self.digraph[x][0].append(y)
            try:
                self.digraph[x][1] = self.digraph[x][1] -1
            except Exception as f:
                raise KeyError(f.message)
            return True
        else:
            return False

    def depth_first_search(self,x,y, z = False, status = 'start'):

        if status == 'start':
            if not z:
                self.visited = [x,y]
            else:
                self.visited = [x,y,z]
        else:
            self.visited.append(x)

        # exclude y (or y,z) in the search
        if not z:
            if x == y:
                raise ValueError('depth_first_search must have two or three different sites')
            for i in self.digraph[x][0]:
                if i not in self.visited:
                    if self.digraph[i][1] > 0:
                        tree = [i]
                        return tree
                    tree = self.depth_first_search(i,y,status='next')
                    if tree:
                        return [i]+tree
        else:
            if x == y or x == z or y == z:
                raise ValueError('depth_first_search must have two or three different sites')
            for i in self.digraph[x][0]:
                if i not in self.visited:
                    if self.digraph[i][1] > 0:
                        tree = [i]
                        return tree
                    tree = self.depth_first_search(i,y, z = z,status='next')
                    if tree:
                        return [i]+tree
        return None


    def collect_one_pebble(self,x,y):

        """
        :param x: a site
        :param y: a different site
        :return: if the one pebble can be collected, return True, otherwise False.
        """

        sites = self.graph.keys()
        if x in sites:
            tree = self.depth_first_search(x,y)
            if tree:
                self.digraph[x][1] += 1
                while tree:
                    site = tree.pop(0)
                    self.digraph[x][0].remove(site)
                    self.digraph[site][0].append(x)
                    x = site
                self.digraph[site][1] += - 1
                return True
            else:
                return False
        else:
            raise ValueError('site %d is not in the lattice.'%x)

    def collect_four_pebble(self, x, y):

        """
        :param x: a site
        :param y: a different site
        :return: if the four pebble can be collected, return True, otherwise False.
        """

        if x == y:
            raise ValueError('collect_four_pebble must have two different sites')

        freex = self.digraph[x][1]
        freey = self.digraph[y][1]
        while freex < 2:
            if self.collect_one_pebble(x,y):
                freex += 1
            else:
                break
        while freey < 2:
            if self.collect_one_pebble(y,x):
                freey += 1
            else:
                break
        if freex==2 and freey==2:
            return True
        else:
            return False




                    




