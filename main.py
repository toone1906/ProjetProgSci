import numpy as np
import pandas as pd 
import matplotlib as plt
import cartopy 
import datetime as t
import tqdm
import math


import json
import part2
#earth = pd.read_fwf("data/Earth_Parameters.dat", skiprows = 8)


with open("data/Tectonic_Plates.geojson") as f:
    Plaques_Techtoniques = json.load(f)

#GSRM = pd.read_fwf("data/GSRM_strain.txt", skiprows=25,  names=["lat","long", "exx","eyy","exy","vorticity","RL-NLC","LL-NLC","e1","e2","azi_e1"] )
ITRF_2020 = pd.read_fwf("data/ITRF2020_GNSS.SSC.txt", skiprows=8,  names=["DOMES NB", "SITE NAME", "TECH","ID", "X/Vx","Y/Vy","Z/Vz","Sigma_x","Sigma_y","Sigma_z","SOLN","DATA_START","DATA_END"] )
pmm_itrf = pd.read_csv("data/pmm_itrf.txt",sep='\s+',skiprows=4,names=["Plate", "Name", "NS","Omega_x", "Omega_y","Omega_z","Omega","WRMS","Sigma_y","s_Omega_x","s_Omega_y","s_Omega_z","s_Omega"])

'''
filtre_pos = (ITRF_2020['DATA_END'] == "00:000:00000") | ((ITRF_2020['DATA_END'].isna()) & (ITRF_2020['SITE NAME'].notna()) )
#je prends une condition sur data_end et les lignes en dessous qui correspond à la vitesse doivent être retirer : notna() enlèbe tout les NaN


last_version_position1 = ITRF_2020.loc[filtre_pos, ['SITE NAME', 'X/Vx','Y/Vy','Z/Vz'] ]
last_version_position1 = last_version_position1.drop_duplicates(subset = 'SITE NAME', keep = 'first')
'''

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
# print(last_version_vitesse)


#Q3 
# Faire une fonction qui nous redonne  λ et φ lorsqu'on reçoit des coordonnées cartésienne en 3 dimension. 

def xyz_to_pol(x,y,z): 
    ae = 6378137.0
    fe = 1/298.257223563
    ee2 = fe*(2-fe)
    r = math.sqrt(x**2 + y**2 + z**2)
    mu = math.atan(z/math.sqrt(x**2+y**2) * ((1-fe) + ae*ee2/r))
    lamb = 2 * math.atan(y / (x + math.sqrt(x**2 + y**2)))
    phi = math.atan((z*(1-fe)+ee2*ae*math.sin(mu)**3 )/((1-fe) * (math.sqrt(x**2 + y**2) - ee2*ae*math.cos(mu)**3)))
    return lamb, phi

#Q4 doit rajouter deux colonnes où on
def rad_to_degres(rad): 
    return rad*180/math.pi
last_version_position2['lon(rad)'] = last_version_position2.apply(lambda r: xyz_to_pol(r['X/Vx'],r['Y/Vy'],r['Z/Vz'])[0], axis = 1)
last_version_position2['lat(rad)'] = last_version_position2.apply(lambda r: xyz_to_pol(r['X/Vx'],r['Y/Vy'],r['Z/Vz'])[1], axis = 1)

last_version_position2['lon(degres)'] = last_version_position2.apply(lambda r : rad_to_degres(r['lon(rad)']),axis = 1 )
last_version_position2['lat(degres)'] = last_version_position2.apply(lambda r : rad_to_degres(r['lat(rad)']), axis = 1)


#print(last_version_position2)


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

last_version_position2['Plate'] = part2.isIn_geoPandas(last_version_position2, dico_plaques_pmm_noms)

print("\nAffichage des stations avec leur plaque tectonique associée :")
print(last_version_position2[['SITE NAME', 'Plate']])
