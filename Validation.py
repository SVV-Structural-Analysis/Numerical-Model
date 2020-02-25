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
nodesdef = np.array(nodes) #make array

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

stcase1 = benskinav[benskinav[:,0].argsort()]          #stress and shear and elementnumbers and elements in right order
stcase2 = jambenskinav[jambenskinav[:,0].argsort()]
stcase3 = jamstrskinav[jamstrskinav[:,0].argsort()]

avelcord = []                               #take average of nodes to get to integration point for plotting
for i in range(0,len(elecord)):
    elcord = np.mean(elecord[i], axis=0)
    avelcord.append(elcord)
avelcord = np.array(avelcord)

defl1 = readdef('Deflection1')              #Deflections
defl2 = readdef('Deflection2')
defl3 = readdef('Deflection3')

RF1 = readdef('RF1')
RF2 = readdef('RF2')                        #Reaction Forces
RF3 = readdef('RF3')
#--------------------------------------------PLOTTING DEFLECTION-------------------------------------------------------
# fig = plt.figure()
# ax = plt.gca(projection='3d')
# ax.set_xlabel('Spanwise Direction')
# ax.set_ylabel('Height')
# ax.set_zlabel('Chordwise Direction')
# ax.set_xlim3d(0,2500)
# ax.set_ylim3d(-500,500)   #-1250,1250
# ax.set_zlim3d(-1000,1000) #-1250,1250
#-------------------------------Plotting Deflection---------------------------------------------------------------------
# x = nodesdef[:,0] + defl1[:,2]*10
# y = nodesdef[:,1] + defl1[:,3]*10
# z = nodesdef[:,2] + defl1[:,4]*10
# pl = ax.scatter(x,y,z,c=defl1[:,1], cmap='coolwarm')
# color = fig.colorbar(pl)
# color.set_label('Deflection')
# plt.show()
#-------------------------------Plotting Stress and Shear---------------------------------------------------------------
# x = avelcord[:,0]
# y = avelcord[:,1]
# z = avelcord[:,2]
# pl = ax.scatter(x,y,z, c=stcase1[:,2], cmap='coolwarm')
# color = fig.colorbar(pl)
# color.set_label('Von Mises Stress')
# plt.show()
#--------------------------------------------COMPARISON NUMMERICAL MODEL------------------------------------------------
'Find maximum stress,shear and deflection'
maxstress = max(stcase1[:,1])
idmaxstress = np.argmax(stcase1[:,1], axis=0)

maxshear = max(stcase1[:,2])
idmaxshear = np.argmax(stcase1[:,2], axis=0)

maxdef = max(defl1[:,1])                                #use magnitude deflection
idmaxdef = np.argmax(defl1[:,1], axis=0)

#kijk naar waardes 95% van de maximum stress, zodat je een region krijgt
# maxreg = []
# cordreg = []
# for k in range(len(stcase1)):
#     if stcase1[k,1] >= 0.92*max(stcase1[:,1]):
#         maxreg.append([stcase1[k,0],stcase1[k,1]])
#         cordreg.append(avelcord[k,:])
# maxreg = np.array(maxreg)
# cordreg = np.array(cordreg)
# print(cordreg, maxreg)

#Need to find hingeline nodes of the aileron
hinge1 = []
index = []
for i in range(len(nodesdef)):
    if nodesdef[i,1] == 0 and nodesdef[i,2] == 0:
        hinge1.append(nodesdef[i,:])
        index.append(i+1)
hinge2 = np.array(hinge1)
index2 = np.vstack(np.array(index))
hinge = np.column_stack((index2,hinge2))  #the nodes and coordinates of the hinge line

deflhinge = []                      #use deflection case1
for j in range(len(defl1)):
    for k in range(len(hinge)):
        if defl1[j,0] == hinge[k,0]:
            deflhinge.append(defl1[j,:])
            break
hingedefl = np.array(deflhinge)         #node number, magnitude, x, y, z
print(hingedefl)
print(hinge)

x = hinge[:,1] + hingedefl[:,2]
y = hinge[:,2] + hingedefl[:,3]
z = hinge[:,3] + hingedefl[:,4]
plt.scatter(x,y)
plt.xlabel('Spanwise Direction [mm]')
# plt.xlabel('Deflection in Z-direction [mm]')
plt.ylabel('Deflection in Y-direction [mm]')
plt.show()
