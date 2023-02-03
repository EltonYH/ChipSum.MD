#user/bin/python3
import numpy as np
import linecache
from scipy.fftpack import fft, fftfreq
import sys

dev = int(sys.argv[1].split("=")[1])
# print(dev)
s = int(sys.argv[2].split("=")[1])
e = int(sys.argv[3].split("=")[1])
step = int(sys.argv[4].split("=")[1])

species = linecache.getline('POSCAR', 6).strip(' ').split()
num_species = linecache.getline('POSCAR', 7).strip(' ').split()
a = linecache.getline('POSCAR', 3).strip(' ').split()

time, f, dos = [], [], []
force_constant = ["start: "+str(s)+" end: "+str(e)]
half = float(a[0])/2.0
dt = 0.5e-15*step         #取样时间间隔s
Fs = (1/dt)*1e-12    #抽样频率THz
h = 1.05457162825177e-34
NA_c = 6.02214076e+23
eV = 1.60217646e-19 #J
T = 3000            #K
kbt = T*0.025852/300 #eV
periodic_mass = {'H': 1.00794, 'He': 4.002602, 'Li': 6.941, 'Be': 9.0121831, 'B': 10.811, 'C': 12.0107, 'N': 14.0067, 'O': 15.9994, 'F': 18.99840316, 'Ne': 20.1797, 'Na': 22.98976928, 'Mg': 24.305, 'Al': 26.9815385, 'Si': 28.0855, 'P': 30.973762, 'S': 32.065, 'Cl': 35.453, 'Ar': 39.948, 'K': 39.0983, 'Ca': 40.078, 'Sc': 44.955908, 'Ti': 47.867, 'V': 50.9415, 'Cr': 51.9961, 'Mn': 54.938044, 'Fe': 55.845, 'Co': 58.933194, 'Ni': 58.6934, 'Cu': 63.546, 'Zn': 65.38, 'Ga': 69.723, 'Ge': 72.64, 'As': 74.921595, 'Se': 78.971, 'Br': 79.904, 'Kr': 83.798, 'Rb': 85.4678, 'Sr': 87.62, 'Y': 88.90584, 'Zr': 91.224, 'Nb': 92.90637, 'Mo': 95.95, 'Tc': 98.9072, 'Ru': 101.07, 'Rh': 102.9055, 'Pd': 106.42, 'Ag': 107.8682, 'Cd': 112.414, 'In': 114.818, 'Sn': 118.71, 'Sb': 121.76, 'Te': 127.6, 'I': 126.90447, 'Xe': 131.293, 'Cs': 132.905452, 'Ba': 137.327, 'La': 138.90547, 'Ce': 140.116, 'Pr': 140.90766, 'Nd': 144.242, 'Pm': 144.9, 'Sm': 150.36, 'Eu': 151.964, 'Gd': 157.25, 'Tb': 158.92535, 'Dy': 162.5, 'Ho': 164.93033, 'Er': 167.259, 'Tm': 168.93422, 'Yb': 173.054, 'Lu': 174.9668, 'Hf': 178.49, 'Ta': 180.94788, 'W': 183.84, 'Re': 186.207, 'Os': 190.23, 'Ir': 192.217, 'Pt': 195.084, 'Au': 196.966569, 'Hg': 200.59, 'Tl': 204.3833, 'Pb': 207.2, 'Bi': 208.9804, 'Po': 208.9824, 'At': 209.9871, 'Rn': 222.0176, 'Fr': 223.0197, 'Ra': 226.0245, 'Ac': 227.0277, 'Th': 232.0377, 'Pa': 231.03588, 'U': 238.02891, 'Np': 237.0482, 'Pu': 239.0642, 'Am': 243.0614, 'Cm': 247.0704, 'Bk': 247.0703, 'Cf': 251.0796, 'Es': 252.083, 'Fm': 257.0591, 'Md': 258.0984, 'No': 259.101, 'Lr': 262.1097, 'Rf': 267.1218, 'Db': 268.1257, 'Sg': 269.1286, 'Bh': 274.1436, 'Hs': 277.1519, 'Mt': 278, 'Ds': 281, 'Rg': 282, 'Cn': 285, 'Nh': 284, 'Fl': 289, 'Mc': 288, 'Lv': 292}

def read_pos(file_name):
    pos =[]
    with open(file_name) as fi:
        for line in fi:
            ll = line.strip(' ').split()
            pos.append(list(map(float, ll[1:])))
    return np.array(pos)

def divide(array, n):
    result = []
    for i in range(n):
        x = array[i::n][:,0].tolist()
        y = array[i::n][:,1].tolist()
        z = array[i::n][:,2].tolist()
        result.append(x);result.append(y);result.append(z);
    return np.array(result)
atm_p_mass = 0.0
for ele in species[:]:
    mass = periodic_mass[ele]
    f_name = ele + '.pos'
    n_ele = int(num_species[species.index(ele)])
    atm_p_mass += n_ele*mass
    if e == 0:
        position = read_pos(f_name)[-s*n_ele:]
    else:
        position = read_pos(f_name)[-s*n_ele:-e*n_ele]
    pos_div = divide(position,n_ele)[:,::step]
    num = np.shape(pos_div)[1]
    if dev == 0:
        vel = pos_div[:,:]*1e-10
        vel2 = np.sum(vel[:]**2)/n_ele/(num-dev)
    elif dev == 1:
        dpos=np.diff(pos_div, n=1, axis=1)
        print(np.max(dpos))
        dpos[dpos > half] -= half*2
        dpos[dpos < -half] += half*2
        vel = dpos*1e-10/dt
        vel2 = np.sum(vel[:]**2)/n_ele/(num-dev)
    elif dev == 2:
        dpos=np.diff(pos_div, n=2, axis=1)
        dpos[dpos > half] -= half*2
        dpos[dpos < -half] += half*2
        vel = dpos*1e-10/dt**2
        vel2 = np.sum(vel[:]**2)/n_ele/(num-dev)
    elif dev == 3:
        dpos=np.diff(pos_div, n=3, axis=1)
        dpos[dpos > half] -= half*2
        dpos[dpos < -half] += half*2
        vel = dpos*1e-10/dt**3
        vel2 = np.sum(vel[:]**2)/n_ele/(num-dev)
    else:
        print("You should give the variable 'dev' as 'python3 script.py dev=0,1,2,3'")
        exit()
    row = np.shape(vel)[0]
    acf_vel = np.zeros((num-dev)*2-1)
    for i in range(row):
        acf_vel += np.correlate(vel[i], vel[i], 'full')
    time = [dt*i for i in range(num-dev)]
    f = fftfreq((num-dev)*2-1, dt)*1e-12
    
    acf_vel_ave = acf_vel[:]/n_ele/3.0
    acf_vel_ave /= vel2/3
    acf_vel_sum = acf_vel[:]/np.sum(vel**2)
    
    fft_acf_ave = np.abs(fft(acf_vel_sum[:]-np.average(acf_vel_sum[:])))
    dos.append(n_ele*mass*fft_acf_ave[:])
    
    EY = fft_acf_ave[:num-dev]/4.13567*1000.0
    EX = f[:num-dev]*4.13567/1000.0
    Y = (EX[:]**2)*EY[:]
    delt = np.diff(EX[:])
    dEY = delt[:]*EY[1:]
    dY = delt[:]*Y[1:]
    IEY = np.sum(dEY[:])
    IY = np.sum(dY[:])
    FC = IY/IEY*mass/1000.0/NA_c*(eV**2)/(h**2)
    print("FC_"+ele+": "+str(FC))
    force_constant.append("FC_"+ele+": "+str(FC))
    
    with open(ele+"_acf_ave.out", "w") as wfe:
        wfe.write("Time/ps    VACF\n")
        for i in range(len(acf_vel_ave[num-dev-1:])):
            wfe.write(str(time[i])+' '+str(acf_vel_ave[num-dev-1+i])+'\n')
    with open(ele+"_acf_sum.out", "w") as wfe:
        wfe.write("Time/ps    VACF\n")
        for i in range(len(acf_vel_sum[num-dev-1:])):
            wfe.write(str(time[i])+' '+str(acf_vel_sum[num-dev-1+i])+'\n')
    
    with open(ele+"_pdos.out", "w") as wfe:
        wfe.write("f/THz    pDOS\n")
        for i in range(len(fft_acf_ave[:num-dev])):
            wfe.write(str(f[i])+' '+str(fft_acf_ave[i])+'\n')
with open("Force_constant_"+str(s)+"-"+str(e)+".log", "w") as wfe:
    for line in force_constant[:]:
        wfe.write(line+'\n')

dos = np.sum(dos[:], axis=0)/atm_p_mass
with open("Total_DOS.out", "w") as wfe:
    wfe.write("f/THz    DOS\n")
    for i in range(len(dos[:num-dev])):
        wfe.write(str(f[i])+' '+str(dos[i])+'\n')
