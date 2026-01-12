import numpy as np

with open("data/Earth_Parameters.dat", 'r') as f: 
    txt = f.readlines()
earth = {}
for i in range (0,len(txt)-1,2):
    earth[txt[i][2:-1]] = txt[i+1][:-1]


def xyz_to_pol(x,y,z): 
    ae = float(earth['ae'])
    fe = 1/float(earth['1/fe'])
    ee2 = fe*(2-fe)
    r = np.sqrt(x**2 + y**2 + z**2)
    mu = np.atan(z/np.sqrt(x**2+y**2) * ((1-fe) + ae*ee2/r))
    lamb = 2 * np.atan(y / (x + np.sqrt(x**2 + y**2)))
    phi = np.atan((z*(1-fe)+ee2*ae*np.sin(mu)**3 )/((1-fe) * (np.sqrt(x**2 + y**2) - ee2*ae*np.cos(mu)**3)))
    return lamb, phi

#Q4 doit rajouter deux colonnes où on
def rad_to_degres(rad): 
    return rad*180/np.pi


def radlon(r): 
    return xyz_to_pol(r['X/Vx'],r['Y/Vy'],r['Z/Vz'])[0]
def radlat(r): 
    return xyz_to_pol(r['X/Vx'],r['Y/Vy'],r['Z/Vz'])[1]
def degreslon(r): 
    return rad_to_degres(xyz_to_pol(r['X/Vx'],r['Y/Vy'],r['Z/Vz'])[0])
def degreslat(r): 
    return rad_to_degres(xyz_to_pol(r['X/Vx'],r['Y/Vy'],r['Z/Vz'])[1])