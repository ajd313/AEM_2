import numpy as np
import math
import operator
import random

import matplotlib.pyplot as plt

def draw_path(nodes):
    nodes.append(nodes[0]) #zamknięcie koła
    nodes = np.array(nodes)
    xc = []
    yc = []
    for n in range(len(nodes)):
        xc.append(nodes[n,1])
        yc.append(nodes[n,2])
    plt.plot(xc,yc)
    plt.show()

def distance(pt1, pt2):
    return math.sqrt((pt1[1] - pt2[1])**2 + (pt1[2] - pt2[2])**2)

def convert_to_int_table(str_nodes):
    return [int(str_nodes[0]), int(str_nodes[1]), int(str_nodes[2])]

def load_instance():
    nodes = []
    with open("kroA100.txt", 'r') as instance:
        str_nodes = instance.readlines()
        nodes = [convert_to_int_table(line[:].replace('\n', "").split(' ')) for line in str_nodes]
        return nodes

def swap_nodes(path, node1, node2):
    path[node1],path[node2] = path[node2],path[node1]
    return path

def swap_line(path, node1, node2):
    if node1 < node2:
        tmp = path[node1:node2]
        path = path[:node1] + tmp[::-1] + path[node2:]
    elif node1 > node2:
        tmp = path[node2:node1]
        path = path[:node2] + tmp[::-1] + path[node1:]
    return path


# --------------------------------------------------------------------

#     A    L    G    O    R    Y    T    M   Y

# --------------------------------------------------------------------
class World:

    def __init__(self, nodes):
        self.nodes = nodes
        DT = np.full((len(nodes),len(nodes)),999999)
        for i in range(len(nodes)):
            for j in range(i+1,len(nodes)):
                DT[i,j] = DT[j,i] = distance(nodes[i],nodes[j])
        self.Distance_MAT = DT
        self.indexes = [node[0] for node in nodes]

    def others(self,path): #returns list of indexes not in path
        return list(set(self.indexes).difference(set(path))).copy()
    
    def gen_random_path(self):
        return random.sample(self.indexes,
                            int(math.floor(len(self.indexes)/2)))

    def calculate_path_length(self,path,close=False):
        length = 0
        for i in range(len(path)-1):
            length += self.Distance_MAT[path[i]-1,path[i+1]-1]
        if close==True:
            length += self.Distance_MAT[path[len(path)]-1,path[0]-1]
        return float("{0:.2f}".format(length))

    def change_node_set(self,path,i,j,others=None):
        if others==None:
            others = self.others(path)
        path[i] = others[j]
        return path

    def steepest_part(self,path,swap_lines=False):
        best_length = self.calculate_path_length(path)
        best_path = path.copy()
        others = self.others(path)
        for i in range(len(path)):
            for j in range(len(others)):
                new_path = path.copy()
                new_path = self.change_node_set(new_path,i,j,others)
                new_length = self.calculate_path_length(new_path)
                if new_length<best_length:
                    best_length=new_length
                    best_path = new_path.copy()
                new_path = path.copy()

                if swap_lines == True:
                    new_path = swap_line(new_path,i,j)
                else:
                    new_path = swap_nodes(new_path,i,j)
                
                new_length = self.calculate_path_length(new_path)
                if new_length<best_length:
                    best_length=new_length
                    best_path = new_path.copy()
        return best_path, best_length

    def greedy_part(self,path,method, rand1, rand2,swap_lines=False):
        length = self.calculate_path_length(path)
        new_path = path.copy()
        others = self.others(path)
        if method == 1:
            new_path = self.change_node_set(new_path,rand1,rand2,others)
            new_length = self.calculate_path_length(new_path)
            if new_length<length:
                return new_path,new_length
        else:
            if swap_lines==True:
                new_path = swap_line(new_path,rand1,rand2)
                new_length = self.calculate_path_length(new_path)
                if new_length<length:
                    return new_path,new_length
            else:
                new_path = swap_nodes(new_path,rand1,rand2)
                new_length = self.calculate_path_length(new_path)
                if new_length<length:
                    return new_path,new_length
        return path,length

    def steepest(self, path, swap_lines=False):
        length = self.calculate_path_length(path)
        path, new_length = self.steepest_part(path,swap_lines)
        while new_length<length:
            length = new_length
            path, new_length = self.steepest_part(path,swap_lines)
        return path, new_length

    def greedy(self, path,swap_lines=False):
        length = self.calculate_path_length(path)
        new_length = length-1
        while new_length<length:
            length=new_length
            rand1 = list(range(int(math.floor(len(self.nodes)/2))))
            rand2 = rand1.copy()
            random.shuffle(rand1)
            random.shuffle(rand2)

            method = [1,0]
            random.shuffle(method)

            for r1 in rand1:
                for r2 in rand2:
                    ipath, new_length = self.greedy_part(path,method[0],r1,r2,swap_lines)
                    if new_length<length:
                        path = ipath.copy()
                        break
                if new_length<length:
                    break
            
            if new_length==length:
                for r1 in rand1:
                    for r2 in rand2:
                        ipath,new_length= self.greedy_part(path,method[1],r1,r2,swap_lines)
                        if new_length<length:
                            path=ipath.copy()
                            break
                    if new_length<length:
                        break
        return path,new_length