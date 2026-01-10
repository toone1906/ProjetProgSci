import pandas as pd 
import math as m 
import numpy as np 


def distance_haversine(phi1,lambda1,phi2,lambda2): 
    Rt = 6378
    return 2*Rt*np.arcsin(np.sqrt(np.sin((phi2-phi1)/2)**2+ np.cos(phi1)*np.cos(phi2)*np.sin((lambda2 - lambda1)/2)**2))

def distance(d):
    if d>50: 
        return False
    return True

def deg_rad(deg):
    return m.pi*deg/180



def proxi(GRSM,ITRF):   

    GRSM['lat_rad'] = np.deg2rad(GRSM['lat'])
    GRSM['long_rad'] = np.deg2rad(GRSM['long'])
    
    # Extraire les arrays numpy pour les calculs vectorisés
    phi_def = GRSM['lat_rad'].values
    lambda_def = GRSM['long_rad'].values
    
    phi_stations = ITRF['lat(rad)'].values
    lambda_stations = ITRF['lon(rad)'].values
    
    # Initialiser le tableau des distances minimales
    n_stations = len(ITRF)
    distance_min = np.full(n_stations, np.inf)
    
    for i in range(n_stations):
        # Broadcasting: calcule toutes les distances d'un coup
        distances = distance_haversine(phi_stations[i], lambda_stations[i], phi_def,lambda_def)
        distance_min[i] = np.min(distances)
    
    # Ajouter les résultats au DataFrame
    ITRF = ITRF.copy()
    ITRF['in_deformation'] = distance_min < 50
    ITRF['min_def'] = distance_min
    return ITRF

