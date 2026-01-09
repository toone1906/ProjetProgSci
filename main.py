import numpy as np
import pandas as pd 
import matplotlib as plt
import cartopy 
import datetime as t
import tqdm
import math

import json
import part2
import part5


with open("data/Earth_Parameters.dat", 'r') as f: 
    txt = f.readlines()
earth = {}
for i in range (0,len(txt)-1,2):
    earth[txt[i][2:-1]] = txt[i+1][:-1]


with open("data/Tectonic_Plates.geojson") as f:
    Plaques_Techtoniques = json.load(f)

colspecs_ITRF = [(0, 9),(10, 25), (26,30),(32, 36),(37, 50),(51, 64),(65, 79),(80, 85),(86, 92),(93, 99),(100, 102),(103, 115),(116, 128)]

#GSRM = pd.read_fwf("data/GSRM_strain.txt", skiprows=25,  names=["lat","long", "exx","eyy","exy","vorticity","RL-NLC","LL-NLC","e1","e2","azi_e1"] )
ITRF_2020 = pd.read_fwf("data/ITRF2020_GNSS.SSC.txt", skiprows=8,colspecs=colspecs_ITRF,  names=["DOMES NB", "SITE NAME", "TECH","ID", "X/Vx","Y/Vy","Z/Vz","Sigma_x","Sigma_y","Sigma_z","SOLN","DATA_START","DATA_END"] )
pmm_itrf = pd.read_csv("data/pmm_itrf.txt",sep='\s+',skiprows=4,names=["Plate", "Name", "NS","Omega_x", "Omega_y","Omega_z","Omega","WRMS","Sigma_y","s_Omega_x","s_Omega_y","s_Omega_z","s_Omega"])


last_version_position2 = ITRF_2020.loc[(ITRF_2020['SITE NAME'].notna())]
#pour retirer toute les lignes qui traitent de la vitesse (la ville n'est pas renseigné donc NaN)

last_version_position2 = last_version_position2.drop_duplicates(subset= 'SITE NAME', keep = 'last' )
#  on ne garde seulement que la derniere update sur la ville, (appliqué au ville + on garde last)


#print(last_version_position1)


#Q2
#Doit prendre la ligne juste en dessous OU on prend la dernière répéttion mais du DOME NB,
#la vitesse à la meme signature d'antenne que la position. 
last_version_vitesse = ITRF_2020.drop_duplicates(subset= 'DOMES NB', keep='last')
last_version_vitesse = last_version_vitesse.loc[:, ['DOMES NB', 'X/Vx', 'Y/Vy','Z/Vz']]

print(last_version_vitesse)


#Q3 
# Faire une fonction qui nous redonne  λ et φ lorsqu'on reçoit des coordonnées cartésienne en 3 dimension. 

def xyz_to_pol(x,y,z): 
    ae = float(earth['ae'])
    fe = 1/float(earth['1/fe'])
    ee2 = fe*(2-fe)
    r = math.sqrt(x**2 + y**2 + z**2)
    mu = math.atan(z/math.sqrt(x**2+y**2) * ((1-fe) + ae*ee2/r))
    lamb = 2 * math.atan(y / (x + math.sqrt(x**2 + y**2)))
    phi = math.atan((z*(1-fe)+ee2*ae*math.sin(mu)**3 )/((1-fe) * (math.sqrt(x**2 + y**2) - ee2*ae*math.cos(mu)**3)))
    return lamb, phi

#Q4 doit rajouter deux colonnes où on
def rad_to_degres(rad): 
    return rad*180/math.pi


def radlon(r): 
    return xyz_to_pol(r['X/Vx'],r['Y/Vy'],r['Z/Vz'])[0]
def radlat(r): 
    return xyz_to_pol(r['X/Vx'],r['Y/Vy'],r['Z/Vz'])[1]
def degreslon(r): 
    return rad_to_degres(xyz_to_pol(r['X/Vx'],r['Y/Vy'],r['Z/Vz'])[0])
def degreslat(r): 
    return rad_to_degres(xyz_to_pol(r['X/Vx'],r['Y/Vy'],r['Z/Vz'])[1])

last_version_position2['lon(rad)'] = last_version_position2.apply(radlon, axis = 1)
last_version_position2['lat(rad)'] = last_version_position2.apply(radlat, axis = 1)

last_version_position2['lon(degres)'] = last_version_position2.apply(degreslon, axis = 1 )
last_version_position2['lat(degres)'] = last_version_position2.apply(degreslat, axis = 1)


print(last_version_position2)


#1.2
# GSRM["deformation"] = np.sqrt(GSRM["exx"]**2 + GSRM["eyy"]**2 + 2 * GSRM["exy"]**2)

# forte_deformation = GSRM[GSRM["deformation"] > 50]

# forte_deformation = forte_deformation.sort_values(by=["lat", "long", "deformation"], ascending=True)

# forte_deformation_sans_doublons = forte_deformation.drop_duplicates(subset=["lat","long"], keep="last")

#1.3
dico_plaques = {}

for feature in Plaques_Techtoniques["features"]:
    nom = feature["properties"]["PlateName"]
    coords = feature["geometry"]["coordinates"]
    
    type = feature["geometry"]["type"]
    
    points = []
    if type == "Polygon":

        points = coords[0]
    elif type == "MultiPolygon":

        for polygon in coords:
            points.extend(polygon[0])
            points.append([np.nan, np.nan])
            
    if len(points) > 0:
        nb_cols = len(points[0])
        
        if nb_cols == 2:
            cols = ["Lon", "Lat"]
        else:
            cols = ["Lon", "Lat", "h"]
            
        df = pd.DataFrame(points, columns=cols)
        
        if "h" in df.columns:
            df = df[["Lat", "Lon", "h"]]
        else:
            df = df[["Lat", "Lon"]]
            df["h"] = 0

        dico_plaques[nom] = df
        
noms_itrf = set(pmm_itrf["Name"].unique())

dico_plaques_pmm_noms = {
    nom: df 
    for nom, df in dico_plaques.items() 
    if nom in noms_itrf
}

# 2.1

gdf_joined = part2.isIn_geoPandas(last_version_position2, "data/Tectonic_Plates.geojson")
test_version = last_version_position2.copy()

test_version['Plate'] = gdf_joined['PlateName']

last_version_position2['Plate'] = part2.isIn_mat(last_version_position2,dico_plaques_pmm_noms)



print("\nAffichage des stations avec leur plaque tectonique associée :")
print(last_version_position2)

part5.afficher_carte_interactive(dico_plaques_pmm_noms, last_version_position2)
