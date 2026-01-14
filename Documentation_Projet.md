# Documentation du Projet

Généré automatiquement pour : main.py, part1.py, part2.py, part3.py, part4.py, part5.py

---

## Fichier : `main.py`

*Aucune fonction ou classe détectée.*

---

## Fichier : `part1.py`

### Fonction : `xyz_to_pol`
> *Pas de documentation.*

### Fonction : `rad_to_degres`
> *Pas de documentation.*

### Fonction : `radlon`
> *Pas de documentation.*

### Fonction : `radlat`
> *Pas de documentation.*

### Fonction : `degreslon`
> *Pas de documentation.*

### Fonction : `degreslat`
> *Pas de documentation.*

---

## Fichier : `part2.py`

### Fonction : `is_point_in_polygon`
> Détermine si un point est à l'intérieur d'un polygone donné en utilisant l'algorithme du ray-casting.
> 
> Args:
>     point_lon (float): Longitude du point.
>     point_lat (float): Latitude du point.
>     polygon_vertices (list of tuples): Une liste de tuples (lon, lat) représentant les sommets du polygone.
> 
> Returns:
>     bool: True si le point est dans le polygone, False sinon.

### Fonction : `find_plate_for_station`
> *Pas de documentation.*

### Fonction : `isIn_it`
> Détermine pour chaque point de df_points dans quelle plaque de df_plaques il se trouve
> en utilisant un algorithme de ray-casting itératif.
> 
> Args:
>     df_points (pd.DataFrame): DataFrame contenant les points avec les colonnes 'lon(degres)' et 'lat(degres)'.
>     df_plaques (dict): Dictionnaire de DataFrames représentant les polygones des plaques.
>     
> Returns:
>     pd.Series: Une série avec le nom de la plaque pour chaque point.

### Fonction : `isIn_mat`
> _summary_
> 
> Args:
>     df_points (_type_): _description_
>     df_plaques (_type_): _description_
> 
> Returns:
>     _type_: _description_

### Fonction : `isIn_geoPandas`
> _summary_
> 
> Args:
>     df_points (_type_): _description_
>     path (_type_): _description_
> 
> Returns:
>     _type_: _description_

---

## Fichier : `part3.py`

### Fonction : `distance_haversine`
> *Pas de documentation.*

### Fonction : `distance`
> *Pas de documentation.*

### Fonction : `deg_rad`
> *Pas de documentation.*

### Fonction : `proxi`
> *Pas de documentation.*

---

## Fichier : `part4.py`

### Fonction : `v_pred`
> *Pas de documentation.*

---

## Fichier : `part5.py`

### Fonction : `carte_monde_statique`
> _summary_
> 
> Args:
>     dico_plaques (_type_): _description_
>     df_stations (_type_): _description_
>     df_GSRM (_type_): _description_

### Fonction : `carte_eurasie_statique`
> _summary_
> 
> Args:
>     dico_plaques (_type_): _description_
>     df_stations (_type_): _description_
>     df_GSRM (_type_): _description_

---

