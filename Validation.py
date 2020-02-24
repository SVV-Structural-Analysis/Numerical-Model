from mpl_toolkits import mplot3d
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
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
#--------------------------------------------CALCULATIONS-------------------------------------------------------------
benskin = read('Bendingskin')
jambenskin = read('Jambendingskin')
jamstrskin = read('Jamstraightskin')

benskinav = average(benskin)       #element, average bending, average shear
jambenskinav = average(jambenskin)
jamstrskinav = average(jamstrskin)

stcase1 = benskinav[benskinav[:,0].argsort()]      #stress and shear case 1 and elementnumbers and elements in right order
stcase2 = jambenskinav[jambenskinav[:,0].argsort()]
stcase3 = jamstrskinav[jamstrskinav[:,0].argsort()]

avelcord = []
for i in range(0,len(elecord)):
    elcord = np.mean(elecord[i], axis=0)
    avelcord.append(elcord)
avelcord = np.array(avelcord)
# avelcord2 = []
# for i in range(0,len(avelcord)):
#     if avelcord[i,1] >= 0:
#         avelcord2.append(avelcord[i,:])
# avelcord2 = np.array(avelcord2)

#--------------------------------------------PLOTTING Bending/Shear----------------------------------------------------
fig = plt.figure()
x = avelcord[:,0]
y = avelcord[:,1]
z = avelcord[:,2]
ax = plt.gca(projection='3d')
pl = ax.scatter(x,y,z, c=stcase3[:,2], cmap='coolwarm')
ax.set_xlabel('X-axis')
ax.set_ylabel('Y-axis')
ax.set_zlabel('Z-axis')
ax.set_xlim3d(0,2500)
ax.set_ylim3d(-1250,1250)
ax.set_zlim3d(-1000,1000)
fig.colorbar(pl)
plt.show()
#--------------------------------------------CALCULATIONS DEFLECTION----------------------------------------------------
# defl1 = readdef('Deflection1')
# defl2 = readdef('Deflection2')
# defl3 = readdef('Deflection3')
# nodesdef = np.array(nodes) #make array
# #--------------------------------------------PLOTTING DEFLECTION----------------------------------------------------
# fig = plt.figure()
# x = nodesdef[:,0] + defl1[:,2]*10
# y = nodesdef[:,1] + defl1[:,3]*10
# z = nodesdef[:,2] + defl1[:,4]*10
# ax = plt.gca(projection='3d')
# pl = ax.scatter(x,y,z,c=defl1[:,1], cmap='coolwarm')
# ax.set_xlabel('X-axis')
# ax.set_ylabel('Y-axis')
# ax.set_zlabel('Z-axis')
# ax.set_xlim3d(0,2500)
# ax.set_ylim3d(-1250,1250)
# ax.set_zlim3d(-1250,1250)
# fig.colorbar(pl)
# plt.show()


