from mpl_toolkits import mplot3d
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

#--------------------------------------------COORDINATES CONNECT TO ELEMENTS--------------------------------------------
nodes = pd.read_csv('B737.txt', delimiter=',',
                    names = ['node_id', 'x', 'y', 'z'],
                    index_col = 0)
elements = pd.read_csv('Elements', delimiter=',',
                       names = ['number', 'node1', 'node2', 'node3', 'node4'],
                       index_col = 0)

# Check dataframes
# print(nodes.head())
# print(elements.head())

# Couple
node_defs = ['node1','node2','node3','node4']
a = [np.array(nodes.loc[elements.loc[nr,node_defs]]) for nr in elements.index]
elecord = np.array(a)

# Check shape
# print(np.array(a).shape)

# Access element number 4
# print(b[0])
#--------------------------------------------DEFINITIONS-------------------------------------------------------
def read(file):
    name = np.genfromtxt(file, delimiter='')
    return np.delete(name,1,1)  # node, jammed straight loc1, bending loc2, shear loc1, shear loc2

def readdef(file):
    name = np.genfromtxt(file, delimiter='')
    return name

def average(case):                          #average for bending and shear
    a = case[:, 0]
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

def avdef(case):                                #average for deflection
    a = case[:,0]
    b = []
    for i in range(0, len(case)):
        av = (case[i, 2] + case[i, 3] + case[i,4]) / 3
        b.append(av)
    e = np.array(b)
    return np.column_stack((a, e))
#--------------------------------------------CALCULATIONS-------------------------------------------------------------
benskin = read('Bendingskin')
jambenskin = read('Jambendingskin')
jamstrskin = read('Jamstraightskin')

benskinav = average(benskin)       #element, average bending, average shear
jambenskinav = average(jambenskin)
jamstrskinav = average(jamstrskin)

stcase1 = np.sort(benskinav,axis=0)       #stress and shear case 1 and elementnumbers and elements in right order
stcase2 = np.sort(jambenskinav,axis=0)
stcase3 = np.sort(jamstrskinav,axis=0)

avelcord = []
for i in range(0,len(elecord)):
    elcord = np.mean(elecord[i], axis=0)
    avelcord.append(elcord)
avelcord = np.array(avelcord)
#--------------------------------------------PLOTTING Bending/Shear----------------------------------------------------
# fig = plt.figure()
# x = avelcord[:,0]
# y = avelcord[:,1]
# z = avelcord[:,2]
# ax = plt.gca(projection='3d')
# pl = ax.scatter(x,y,z, c=stcase2[:,1], cmap='hsv')
# ax.set_xlabel('X-axis')
# ax.set_ylabel('Y-axis')
# ax.set_zlabel('Z-axis')
# fig.colorbar(pl)
# plt.show()
#--------------------------------------------CALCULATIONS DEFLECTION----------------------------------------------------
defl1 = readdef('Deflection1')
defl2 = readdef('Deflection2')
defl3 = readdef('Deflection3')

defl1av = avdef(defl1)    #node, average deflection
defl2av = avdef(defl2)
defl3av = avdef(defl3)
nodesdef = np.array(nodes)
#--------------------------------------------PLOTTING DEFLECTION----------------------------------------------------
fig = plt.figure()
x = nodesdef[:,0]
y = nodesdef[:,1]
z = nodesdef[:,2]
ax = plt.gca(projection='3d')
pl = ax.scatter(x,y,z, c=defl2av[:,1], cmap='hsv')
ax.set_xlabel('X-axis')
ax.set_ylabel('Y-axis')
ax.set_zlabel('Z-axis')
fig.colorbar(pl)
plt.show()


