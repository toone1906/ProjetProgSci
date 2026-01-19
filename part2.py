import pandas as pd 
import matplotlib as plt
from tqdm import tqdm
import numpy as np
import geopandas 

def is_point_in_polygon(point_lon, point_lat, polygon_vertices):
    """
    Détermine si un point est à l'intérieur d'un polygone donné en utilisant l'algorithme du ray-casting.

    Args:
        point_lon (float): Longitude du point.
        point_lat (float): Latitude du point.
        polygon_vertices (list of tuples): Une liste de tuples (lon, lat) représentant les sommets du polygone.

    Returns:
        bool: True si le point est dans le polygone, False sinon.
    """
    
    n = len(polygon_vertices)
    inside = False

    p1_lon, p1_lat = polygon_vertices[0]
    for i in range(n + 1):
        p2_lon, p2_lat = polygon_vertices[i % n]

        # Vérifie si le rayon horizontal coupe le segment
        if point_lat > min(p1_lat, p2_lat):
            if point_lat <= max(p1_lat, p2_lat):
                if point_lon <= max(p1_lon, p2_lon):
                    if p1_lat != p2_lat:
                        # Calcule l'intersection du rayon avec le segment
                        xinters = (point_lat - p1_lat) * (p2_lon - p1_lon) / (p2_lat - p1_lat) + p1_lon
                        # Si le point est à gauche de l'intersection, c'est un croisement
                        if p1_lon == p2_lon or point_lon <= xinters:
                            inside = not inside
        p1_lon, p1_lat = p2_lon, p2_lat

    return inside
    

def find_plate_for_station(station_lon, station_lat, plates_dict):
    for plate_name, plate_df in plates_dict.items():
        polygon_vertices = plate_df[['Lon', 'Lat']].values.tolist()
        if is_point_in_polygon(station_lon, station_lat, polygon_vertices):
            return plate_name
    return 'Unknown'
def isIn_it(df_points, df_plaques):
    """
    Détermine pour chaque point de df_points dans quelle plaque de df_plaques il se trouve
    en utilisant un algorithme de ray-casting itératif.
    
    Args:
        df_points (pd.DataFrame): DataFrame contenant les points avec les colonnes 'lon(degres)' et 'lat(degres)' des stations GNSS.
        df_plaques (dict): Dictionnaire de DataFrames représentant les polygones des plaques.
        
    Returns:
        pd.Series: Une série avec le nom de la plaque pour chaque point.
    """


    results = []
    
    for index, row in tqdm(df_points.iterrows(), total=df_points.shape[0], desc="Assignation des plaques aux stations"):
        plate = find_plate_for_station(row['lon(degres)'], row['lat(degres)'], df_plaques)
        results.appfin(plate)

    return pd.Series(results, index=df_points.index)

def isIn_mat(df_points, df_plaques):
    """
    Détermine pour chaque point de df_points dans quelle plaque de df_plaques il se trouve
    en utilisant un algorithme de ray-casting matriciel avec numpy.

    Args:
        df_points (pd.DataFrame): DataFrame contenant les points avec les colonnes 'lon(degres)' et 'lat(degres)' des stations GNSS.
        df_plaques (dict): Dictionnaire de DataFrames représentant les polygones des plaques.

    Returns:
        pd.Series: Une série avec le nom de la plaque pour chaque point.
    """
    p_lon = df_points['lon(degres)'].values.reshape(-1, 1)
    p_lat = df_points['lat(degres)'].values.reshape(-1, 1)
    
    n_points = len(df_points)
    results = np.full(n_points, 'Unknown', dtype=object)

    for plate_name, plate_df in tqdm(df_plaques.items(), desc="Assignation des plaques (matriciel)"):

        poly_lon = plate_df['Lon'].values
        poly_lat = plate_df['Lat'].values
        
        # permet de relier chaque point au suivant (et le dernier au premier)
        poly_lon_next = np.roll(poly_lon, -1)
        poly_lat_next = np.roll(poly_lat, -1)

        cond_lat = (poly_lat > p_lat) != (poly_lat_next > p_lat)

        with np.errstate(divide='ignore', invalid='ignore'):
            intersect_lon = ( poly_lon + (p_lat - poly_lat) * (poly_lon_next - poly_lon) / (poly_lat_next - poly_lat))
            
        # Vérification si le point est à gauche de l'intersection
        cond_lon = p_lon < intersect_lon
        
        # valide si les deux conditions sont réunies
        valid_intersections = cond_lat & cond_lon
        
        # Comptage des intersections pour chaque point
        intersections_count = np.sum(valid_intersections, axis=1)
        is_inside = (intersections_count % 2) == 1

        mask_assign = is_inside & (results == 'Unknown')
        results[mask_assign] = plate_name
        
    return pd.Series(results, index=df_points.index)

def isIn_geoPandas(df_points, path):
    """
    Détermine pour chaque point de df_points dans quelle plaque de df_plaques il se trouve
    en utilisant la librairie geopandas qui utilise une version améliorée du ray-casting.

    Args:
        df_points (pd.DataFrame): DataFrame contenant les points avec les colonnes 'lon(degres)' et 'lat(degres) des stations GNSS'.
        path (stcercle): Chemin d'accès du fichier des plaques tectoniques

    Returns:
        geopandas.Geodataframe: Objet geodataframe jonction entre les plaques tectoniques et les stations GNSS
    """
    gdf_points = geopandas.GeoDataFrame(df_points, geometry=geopandas.points_from_xy(df_points['lon(degres)'], df_points['lat(degres)']), crs="EPSG:4326")
    gdf_plaques = geopandas.read_file(path)
    
    return geopandas.sjoin(gdf_points, gdf_plaques, how="left", predicate="intersects")

def point_in_polygon_angle(lat, lon, polygon):
    """
    Détermine si un point est dans un polygone via la méthode de la somme des angles.
    
    Args:
        lat (float): Latitude du point.
        lon (float): Longitude du point.
        polygon (np.array): Tableau numpy des sommets du polygone.
    
    Returns:
        bool: True si le point est à l'intérieur.
    """
    P = np.array([lon, lat])
    total_angle = 0.0
    
    # Gestion des MultiPolygones séparés par des NaNs dans l'ouverture du fichier précédement
    if np.isnan(polygon).any():
        nans = np.isnan(polygon[:, 0])
        sep = np.where(nans)[0]
        lim = np.concatenate(([-1], sep, [len(polygon)]))
    else:
        lim = np.array([-1, len(polygon)])
        
    for i in range(len(lim) - 1):
        debut = lim[i] + 1
        fin = lim[i+1]
        
        if fin > debut:
            cercle = polygon[debut:fin]
            if len(cercle) >= 3:
                U = cercle - P
                V = np.roll(U, -1, axis=0)
                mult = U[:, 0] * V[:, 1] - U[:, 1] * V[:, 0]
                scalaire = U[:, 0] * V[:, 0] + U[:, 1] * V[:, 1]
                total_angle += np.sum(np.arctan2(mult, scalaire))

    return np.isclose(np.abs(total_angle), 2 * np.pi)

def isIn_angle(df_points, dico_plaques):
    """
    Détermine pour chaque point de df_points dans quelle plaque il se trouve en utilisant la méthode de la somme des angles.
    
    Args:
        df_points (pd.DataFrame): DataFrame des points.
        dico_plaques (dict): Dictionnaire des plaques (DataFrames).
        
    Returns:
        pd.Series: Série des noms de plaques trouvées.
    """
    results = []
    
    for i, row in tqdm(df_points.iterrows(), total=len(df_points), desc="Assignation (Angle)"):
        lat = row['lat(degres)']
        lon = row['lon(degres)']
        nom = 'Unknown'
        
        for name, df_plate in dico_plaques.items():
            # Conversion en numpy array des sommets [Lon, Lat]
            poly_arr = df_plate[['Lon', 'Lat']].values
            if point_in_polygon_angle(lat, lon, poly_arr):
                nom = name
                break
        results.append(nom)
        
    return pd.Series(results, index=df_points.index)