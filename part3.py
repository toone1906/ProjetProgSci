import pandas as pd 
import math as m 
import numpy as np 


def distance_haversine(phi1,lambda1,phi2,lambda2): 
    """_summary_
 
    Args:
        Docstring for distance_haversine
    on pose la distance haversine permettant sur un repère geographique d'avoir la distance entre deux points sur une spère
    
    :float phi1:  en radian, information du point 1 sur la latitude
    :flaot lambda1:  en radian, information du point 1 sur la longitude
    :float phi2:  en radian, information du point 2 sur la latitude
    :float lambda2:  en radian, information du point 2 sur la longitude


    Returns:
        :float: distance haversine entre deux points 
    """
    Rt = 6378
    return 2*Rt*np.arcsin(np.sqrt(np.sin((phi2-phi1)/2)**2+ np.cos(phi1)*np.cos(phi2)*np.sin((lambda2 - lambda1)/2)**2))

def distance(d):
    """_summary_
    condition sur la distance, renvoie un booléen
    Args:
        d (float):distance haversine calculé

    Returns:
        bool: si elle dépasse 50 false, sinon True
    """
    
    if d>50: 
        return False
    return True

def deg_rad(deg):
    """_summary_
    passer de deg à radian
    Args:
        deg (float ou np_array): le degres
 
    Returns:
        float ou np_array: en radian
    """
    return np.pi*deg/180



def proxi(GRSM,ITRF):   
    """_summary_
    calcul matriciel pour la distance entre chaque point et les zones de déformation, utilisation de tableau numpy 
    pour éviter les itérations de l'ordre du milion mal optimisées.
    Args:
        GRSM (dataframe): info sur les zones de déforamtion
        ITRF (dataframe): info sur les stations ITRF

    Returns:
        dataframe: ITRF enrichie des booleens si la statio est dans un rayon de 50 km autour d'une zone de déformation. 
    """

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

