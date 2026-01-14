# Documentation du Projet

Généré automatiquement pour : main.py, part1.py, part2.py, part3.py, part4.py, part5.py

---

## Fichier : `main.py`

*Aucune fonction ou classe détectée.*

---

## Fichier : `part1.py`

### Fonction : `xyz_to_pol`
> Convertit des coordonnées cartésiennes ECEF (X, Y, Z) (Earth-Centered, Earth-Fixed) 
> en coordonnées géographiques (longitude λ, latitude φ) sur un ellipsoïde de référence.
> 
> Les coordonnées d'entrée sont supposées exprimées dans un repère ECEF
> centré sur la Terre. L'ellipsoïde de référence
> est défini via le dictionnaire global `earth`, contenant :
>   - earth['ae']    : demi-grand axe a (en mètres)
>   - earth['1/fe']  : inverse de l'aplatissement (1/f)
> 
> 
> :param: x, y, z : array_like
>     Coordonnées cartésiennes ECEF. Peuvent être des scalaires ou des tableaux
>     NumPy (formes compatibles entre elles). Unité : mètres.
> 
> :rtype: lamb, phi
>     retour des coordonnées géogrpaghiques, sous formes de tableaux numpy ou scalaire. unité : radian. 

### Fonction : `rad_to_degres`
> renvoie le tableau le scalire en degres
> 
> :param rad:  l'angle à convertir en degres
> 
> :rtype: le tableau ou le scalaire en degres 

### Fonction : `radlon`
> utilisé dans le main pour passer toutes les coordonées cartésienne des différentes stations en coordonnées
> géographiques (puis de radian à degres), sans passer par une fonction annonyme on utilise alors ses 4 fonctions pour être utilisé dans 
> le .apply de pandas
> 
> :param r: correspond à la ligne appelé dans le dataframe à chaque fois c'est une série de 3 colonnes qui est appelé
> 
> :rtype: le lamb ou long obtenu pour la station en question 

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
>     df_points (pd.DataFrame): DataFrame contenant les points avec les colonnes 'lon(degres)' et 'lat(degres)' des stations GNSS.
>     df_plaques (dict): Dictionnaire de DataFrames représentant les polygones des plaques.
>     
> Returns:
>     pd.Series: Une série avec le nom de la plaque pour chaque point.

### Fonction : `isIn_mat`
> Détermine pour chaque point de df_points dans quelle plaque de df_plaques il se trouve
> en utilisant un algorithme de ray-casting matriciel avec numpy.
> 
> Args:
>     df_points (pd.DataFrame): DataFrame contenant les points avec les colonnes 'lon(degres)' et 'lat(degres)' des stations GNSS.
>     df_plaques (dict): Dictionnaire de DataFrames représentant les polygones des plaques.
> 
> Returns:
>     pd.Series: Une série avec le nom de la plaque pour chaque point.

### Fonction : `isIn_geoPandas`
> Détermine pour chaque point de df_points dans quelle plaque de df_plaques il se trouve
> en utilisant la librairie geopandas qui utilise une version améliorée du ray-casting.
> 
> Args:
>     df_points (pd.DataFrame): DataFrame contenant les points avec les colonnes 'lon(degres)' et 'lat(degres) des stations GNSS'.
>     path (string): Chemin d'accès du fichier des plaques tectoniques
> 
> Returns:
>     geopandas.Geodataframe: Objet geodataframe jonction entre les plaques tectoniques et les stations GNSS

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
> Calcul la vitesse des stations GNSS à partir d'un modèle, puis convertit 
> la vitesse du repère ECEF (XYZ) vers le repère local ENU (East, North, Up).
> Indispensable pour projeter les vecteurs sur la carte de cartopy.
> 
> Le modèle vectoriel utilisé est :
>     v_xyz = ω x r + T
> où :
>   - r = (X, Y, Z) est la position ECEF de la station (m),
>   - ω = (Ωx, Ωy, Ωz) est le vecteur de rotation de la plaque (mas/yr),
>   - T est une constante terrestre de translation (m/yr),
>   - v_xyz est la vitesse prédite en ECEF (m/yr).
> 
> La conversion en ENU est faite au point de la station (défini par sa
> longitude λ et latitude φ, obtenues via `part1.xyz_to_pol(X, Y, Z)`),
> par une rotation orthonormée (la norme de la vitesse est conservée).
> 
> :param: 
> pmm : pandas.DataFrame
>     Table des paramètres de plaques. Contient en particulier:
>       - 'Name' : identifiant de plaque (clé de jointure)
>       - 'Omega_x', 'Omega_y', 'Omega_z' : composantes de ω en mas/yr
> 
>     
> 
> ITRF : pandas.DataFrame
>     Table des stations. Contient en particulier :
>       - 'Plate' : identifiant de plaque associée à la station
>       - 'X/Vx', 'Y/Vy', 'Z/Vz' : coordonnées ECEF de la station (m)
> 
>       Hypothèse : une seule plaque par station, soit plusieurs station sur une meme plaque 
>       mais pas l'inverse, échoue alors avec `validate="m:1"`
> 
> Returns
> -------
> ITRFcop : pandas.DataFrame
>     Copie de `ITRF` enrichie avec :
>       - 'VE', 'VN', 'VU' : composantes de la vitesse prédite en ENU (m/yr)
> 
>     La fonction ne conserve pas explicitement les composantes ECEF dans des
>     colonnes (Vx_pred, Vy_pred, Vz_pred), mais elles sont calculées en
>     interne.
>     Valeurs parfaitement inutile 
> 
> Cependant à utiliser plus tard en vue d'un z_score.

---

## Fichier : `part5.py`

### Fonction : `carte_monde_statique`
> Génération d'une image d'une carte statique du monde avec Matplotlib 
> 
> Args:
>     dico_plaques (dico): Dictionnaire de DataFrames représentant les polygones des plaques.
>     df_stations (pd.dataframe): DataFrame contenant les points avec les colonnes 'lon(degres)' et 'lat(degres) des stations GNSS'.
>     df_GSRM (pd.dataframe): DataFrame contenant les points avec les colonnes 'lon(degres)' et 'lat(degres) des points de deformation'.

### Fonction : `carte_eurasie_statique`
> Génération d'une image d'une carte statique de l'eurasie avec Matplotlib 
> 
> Args:
>     dico_plaques (dico): Dictionnaire de DataFrames représentant les polygones des plaques.
>     df_stations (pd.dataframe): DataFrame contenant les points avec les colonnes 'lon(degres)' et 'lat(degres) des stations GNSS'.
>     df_GSRM (pd.dataframe): DataFrame contenant les points avec les colonnes 'lon(degres)' et 'lat(degres) des points de deformation'.

---

