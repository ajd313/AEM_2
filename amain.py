from aeim import *

import time

paths = []
world = World(load_instance())
repeat = list(range(int(len(world.nodes)/4)))

options = ['steepest_node', 'steepest_line', 'greedy_node', 'greedy_line']

for i in repeat:
    path1 = world.gen_random_path()
    paths.append(path1)

####### steepest
# vertex
def results(option):
    best_length = best_time = 999999999
    worst_length = avg_length = worst_time = avg_time = 0

    for i in repeat:
        path = paths[i]
        
        start = time.time()
        if option == 'steepest_node':
            path1, length1 = world.steepest(path,False)
        elif option == 'steepest_line':
            path1, length1 = world.steepest(path,True)
        elif option == 'greedy_node':
            path1, length1 = world.greedy(path,False)
        elif option == 'greedy_line':
            path1,length1 = world.greedy(path,True)

        end = time.time()
        t1 = end - start

        avg_length += length1/len(repeat)
        avg_time += t1/len(repeat)
        if length1<best_length:
            best_length = length1
            best_path = path1.copy()
        if length1>worst_length:
            worst_length=length1
        if t1<best_time:
            best_time=t1
        if t1>worst_time:
            worst_time=t1
        
    f = open(option+'.txt','a')
    f.write('Best length: ' + str(best_length) + '\n')
    f.write('Worst length: ' + str(worst_length) + '\n')
    f.write('Average length: ' + str(avg_length) + '\n')
    f.write('Best time: ' + str(best_time) + '\n')
    f.write('Worst time: ' + str(worst_time) + '\n')
    f.write('Average time: ' + str(avg_time) + '\n' + '\n')

    return best_path



b = []
bl = 999999
wl = 0
avgl = 0
iter = 0
start = time.time()
while True:
    iter+=1
    path1 = world.gen_random_path()
    length1 = world.calculate_path_length(path1)
    if length1<bl:
        bl = length1
        b = path1.copy()
    if length1>wl:
        wl = length1
    avgl += length1
    end = time.time()
    if end-start > 17:
        break
avgl /= iter
f = open('random_result.txt','a')
f.write('Best length: ' + str(bl) + '\n')
f.write('Worst length: ' + str(wl) + '\n')
f.write('Average length: ' + str(avgl) + '\n'+'\n')
    
def plot_results(nodes,result):
    nodes_xy = np.array([node[1:3] for node in nodes]).T
    xa = nodes_xy[0]
    ya = nodes_xy[1]
    plt.plot(xa,ya,'bo')
    xr = []
    yr = []
    for i in result:
        xr.append(nodes[i-1][1])
        yr.append(nodes[i-1][2])
    plt.plot(xr,yr)
    plt.show()


plot_results(world.nodes,b)
for option in options:
    best_result = results(option)
    plot_results(world.nodes, best_result)
