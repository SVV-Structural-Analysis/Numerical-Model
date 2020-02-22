from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def is_float(string):
    """ True if given string is float else False"""
    try:
        return float(string)
    except ValueError:
        return False

#--------------------------------------------COORDINATES-------------------------------------------------------
nodes = []
with open('B737.txt', 'r') as f:
    d = f.readlines()
    for i in d:
        k = i.rstrip().split(",")
        nodes.append([float(i) if is_float(i) else i for i in k])

nodes = np.array(nodes, dtype='O') #node, x, y ,z

# print(nodes[:,1]) #prints column 1(y) as a row
# print(nodes[0,:]) #prints first row as a row

#--------------------------------------------DEFINITIONS-------------------------------------------------------
def read(file):
    name = []
    with open(file, 'r') as f:
        d = f.readlines()
        for i in d:
            k = i.rstrip().split()
            name.append([float(i) if is_float(i) else i for i in k])

    name = np.array(name, dtype='O')  # jammed straight on spar
    return np.delete(name, 1, 1)  # node, jammed straight loc1, bending loc2, shear loc1, shear loc2

def average(case):
    a = case[:, 0] #lol
    b = []
    c = []
    for i in range(0, len(case)):
        av = (case[i, 1] + case[i, 2]) / 2
        b.append(av)
        avs = (case[i, 3] + case[i, 4]) / 2
        c.append(avs)
    e = np.array(b)
    f = np.array(c)
    return np.column_stack((a, e, f))

def compare(node, case):
    coord = []
    values = []
    for i in range(0,len(case)):
        for k in range(0,len(node)):
            if case[i,0] ==  node[k,0]:
                coord.append([node[k,1],node[k,2], node[k,3]])
                values.append([case[i,1],case[i,2]])
                break
    a = np.array(coord)
    b = np.array(values)
    a = a.astype(np.float)
    return a,b

#--------------------------------------------CALCULATIONS-------------------------------------------------------------

benskin = read('Bendingskin')
benspar = read('bendingspar')
jambenskin = read('Jambendingskin')
jambenspar = read('Jambendingspar')
jamstrskin = read('Jamstraightskin')
jamstrspar = read('Jamstraightspar')

benskinav = average(benskin)
bensparav = average(benspar)        #node, average bending, average shear
jambenskinav = average(jambenskin)
jambensparav = average(jambenspar)
jamstrskinav = average(jamstrskin)
jamstrsparav = average(jamstrspar)

#--------------------------------------------PLOTTING----------------------------------------------------------------

case1a = compare(nodes,benskinav)
case1acord = case1a[0]
case1aval = case1a[1]

case1b = compare(nodes,bensparav)
case1bcord = case1b[0]
case1bval = case1b[1]

case1cord = np.concatenate((case1acord,case1bcord))
case1val = np.concatenate((case1aval,case1bval))

fig = plt.figure()
x = case1cord[:,0]
y = case1cord[:,1]
z = case1cord[:,2]
ax = plt.gca(projection='3d')
ax.scatter(x,y,z, c=case1val[:,0])
ax.set_xlabel('X-axis')
ax.set_ylabel('Y-axis')
ax.set_zlabel('Z-axis')

plt.show()



