#user/bin/python3
import numpy as np
import linecache, sys

#####################################################################################################
#               Calculate bond length from VASP MD                                                  #
#  1. This code is suggested to be used after MSDVASP.py and the POSCAR should be in the directory; #
#  2. The variables you should modify is 'file1','file2','atom1','atom2' and 'count'. file1 and     #
#     and file2 are the position file of selected atoms which are generated by MSDVASP.py code.     #
#     atom1 and atom2 are the atoms you selected will be calculated the bond of atom1-atom2. count  #
#     is the number of the output bonds you want write in '.out' file.                              #
#####################################################################################################


atom1 = sys.argv[1].title()
atom2 = sys.argv[2].title()
file1, file2 = atom1+'.pos', atom2+'.pos'
count = 10
bond_cut = 3.0

out = []
alatx = linecache.getline('POSCAR', 3).strip(' ').split()
alaty = linecache.getline('POSCAR', 4).strip(' ').split()
alatz = linecache.getline('POSCAR', 5).strip(' ').split()
alat = [[float(alatx[0]),float(alatx[1]),float(alatx[2])],
        [float(alaty[0]),float(alaty[1]),float(alaty[2])],
        [float(alatz[0]),float(alatz[1]),float(alatz[2])]]
species = linecache.getline('POSCAR', 6).strip(' ').split()
num_species = linecache.getline('POSCAR', 7).strip(' ').split()
if atom1 not in species or atom2 not in species:
  print("Error, the atom you selected is not in the system!")
  exit()
site1, site2 = species.index(atom1), species.index(atom2)
num1, num2 = int(num_species[site1]), int(num_species[site2])
pos1, pos2 = [], []
print(atom1+': '+str(num1)+'; '+atom2+': '+str(num2))

with open(file1) as file:
  for line in file:
    ll = line.strip(' ').split()
    pos1.append(list(map(float, ll[1:])))

with open(file2) as file:
  for line in file:
    ll = line.strip(' ').split()
    pos2.append(list(map(float, ll[1:])))

num_conf1, num_conf2 = int(len(pos1)/num1), int(len(pos2)/num2)
print(str(num_conf1)+'; '+str(num_conf2))
if num_conf1 != num_conf2:
  print("Error, these two species give different number of configurations!")
  exit()

tr_ma = []
for i in (-1, 0, 1):
  for j in (-1, 0, 1):
    for k in (-1, 0, 1):
      tr_ma.append(np.array([i,j,k]))

def supcell(position,ca):
  array = np.array(position)
  new_position = []
  for mi in tr_ma:
    new_pos = array+np.dot(mi, ca)
    new_position = new_position + new_pos.tolist()
  return new_position

def calbond(aposition, bposition):
  la, lb = len(aposition), len(bposition)
  arraya = np.array(aposition)
  arrayb = np.array(bposition)
  bond_len = []
  for i in range(la):
    posa = np.array([arraya[i].tolist()]*lb)
    bd0 = (posa - arrayb).tolist()
    bd1 = np.array(supcell(bd0, alat))
    bond = np.sqrt(np.sum(bd1**2, axis=1))
    bond_len.append(sorted(bond.tolist()))
  return bond_len

for x in range(1, num_conf1+1):
  if x%100 == 0:
    print(x)
  bl = calbond(pos1[(x-1)*num1:x*num1], pos2[(x-1)*num2:x*num2])
  out.append(bl)
print(np.array(out).shape)
for i in range(num1):
  ofile = atom1+str(i+1)+'-'+atom2+'.out'
  with open(ofile, "w") as wfe:
    for j in range(num_conf1):
      cn = 0
      for k in range(count):
        wfe.write(str(out[j][i][k])+", ")
        if out[j][i][k] <= bond_cut:
          cn = cn + 1
      wfe.write("CN:"+str(cn)+"\n")
if num1 > 1:
    ave_out = np.sum(out, axis=1)/num1
    file_ave = atom1+'-'+atom2+'_average.out'
    with open(file_ave, "w") as wfe:
        for j in range(num_conf1):
            cn = 0
            for k in range(count):
                wfe.write(str(ave_out[j][k])+", ")
                if ave_out[j][k] <= bond_cut:
                    cn = cn + 1
            wfe.write("CN:"+str(cn)+"\n")