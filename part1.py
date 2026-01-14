import numpy as np

with open("data/Earth_Parameters.dat", 'r') as f: 
    txt = f.readlines()
earth = {}
for i in range (0,len(txt)-1,2):
    earth[txt[i][2:-1]] = txt[i+1][:-1]     #création d'un disctionnaire avec les données et valeurs importante pour les calculs


def xyz_to_pol(x,y,z): 
    '''
    Convertit des coordonnées cartésiennes ECEF (X, Y, Z) (Earth-Centered, Earth-Fixed) 
    en coordonnées géographiques (longitude λ, latitude φ) sur un ellipsoïde de référence.

    Les coordonnées d'entrée sont supposées exprimées dans un repère ECEF
    centré sur la Terre. L'ellipsoïde de référence
    est défini via le dictionnaire global `earth`, contenant :
      - earth['ae']    : demi-grand axe a (en mètres)
      - earth['1/fe']  : inverse de l'aplatissement (1/f)

    
    :param: x, y, z : array_like
        Coordonnées cartésiennes ECEF. Peuvent être des scalaires ou des tableaux
        NumPy (formes compatibles entre elles). Unité : mètres.

    :rtype: lamb, phi
        retour des coordonnées géogrpaghiques, sous formes de tableaux numpy ou scalaire. unité : radian. 
    '''

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
    '''
    renvoie le tableau le scalire en degres
    
    :param rad:  l'angle à convertir en degres

    :rtype: le tableau ou le scalaire en degres 
    '''
    return rad*180/np.pi


def radlon(r): 
    '''
    utilisé dans le main pour passer toutes les coordonées cartésienne des différentes stations en coordonnées
    géographiques (puis de radian à degres), sans passer par une fonction annonyme on utilise alors ses 4 fonctions pour être utilisé dans 
    le .apply de pandas
    
    :param r: correspond à la ligne appelé dans le dataframe à chaque fois c'est une série de 3 colonnes qui est appelé

    :rtype: le lamb ou long obtenu pour la station en question 
    '''
    return xyz_to_pol(r['X/Vx'],r['Y/Vy'],r['Z/Vz'])[0]
def radlat(r): 
    return xyz_to_pol(r['X/Vx'],r['Y/Vy'],r['Z/Vz'])[1]
def degreslon(r): 
    return rad_to_degres(xyz_to_pol(r['X/Vx'],r['Y/Vy'],r['Z/Vz'])[0])
def degreslat(r): 
    return rad_to_degres(xyz_to_pol(r['X/Vx'],r['Y/Vy'],r['Z/Vz'])[1])