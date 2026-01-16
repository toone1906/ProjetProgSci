# Documentation du Projet

Généré automatiquement pour : main.py, part1.py, part2.py, part3.py, part4.py, part5.py

---

## Fichier : `main.py`

*Aucune fonction ou classe détectée.*

---

## Fichier : `part1.py`

### Fonction : `xyz_to_pol`
> _summary_
> Convertit des coordonnées cartésiennes ECEF (X, Y, Z) (Earth-Centered, Earth-Fixed) 
> en coordonnées géographiques (longitude λ, latitude φ) sur un ellipsoïde de référence.
> 
> Les coordonnées d'entrée sont supposées exprimées dans un repère ECEF
> centré sur la Terre. L'ellipsoïde de référence
> est défini via le dictionnaire global `earth`, contenant :
>   - earth['ae']    : demi-grand axe a (en mètres)
>   - earth['1/fe']  : inverse de l'aplatissement (1/f)
> 
> Args:
>     x (np.array): Coordonnées cartésiennes ECEF. Peuvent être des scalaires ou des tableaux
>     NumPy (formes compatibles entre elles). Unité : mètres.
>     y (np.array): //
>     z (np.array): //
> 
> Returns:
>     lamb,phi(np.array): retour des coordonnées géogrpaghiques, sous formes de tableaux numpy 
>                           ou scalaire. unité : radian. 

### Fonction : `rad_to_degres`
> _summary_
> renvoie le tableau le scalire en degres
> Args:
>     rad (float):  l'angle à convertir en degres
> 
> Returns:
>     float:le tableau ou le scalaire en degres 

### Fonction : `radlon`
> _summary_
> utilisé dans le main pour passer toutes les coordonées cartésienne des différentes stations en coordonnées
> géographiques (puis de radian à degres), sans passer par une fonction annonyme on utilise alors ses 4 fonctions pour être utilisé dans 
> le .apply de pandas
> 
> Args:
>     r (series (ligne de DataFrame)):correspond à la ligne appelé dans le dataframe à chaque fois c'est une série de 3 colonnes qui est appelé 
> 
> Returns:
>     series: le lamb ou long obtenu pour la station en question  en coordonnés et polaire

### Fonction : `radlat`
> _summary_
> utilisé dans le main pour passer toutes les coordonées cartésienne des différentes stations en coordonnées
> géographiques (puis de radian à degres), sans passer par une fonction annonyme on utilise alors ses 4 fonctions 
> pour être utilisé dans le .apply de pandas
> 
> Args:
>     r (series (ligne de DataFrame)):correspond à la ligne appelé dans le dataframe à 
>                                     chaque fois c'est une série de 3 colonnes qui est appelé 
> 
> Returns:
>     series: le lamb ou long obtenu pour la station en question  en coordonnés et polaire donc en radian

### Fonction : `degreslon`
> _summary_
> Il faut avoir les valeurs en degrés 
> Args:
>     r (series (ligne de DataFrame)):correspond à la ligne appelé dans le dataframe
>                                     à chaque fois c'est une série de 3 colonnes qui est appelé 
> 
> Returns:
>     series: meme chose que radlat mais degres

### Fonction : `degreslat`
> _summary_
> Il faut avoir les valeurs en degrés 
> Args:
>     r (series (ligne de DataFrame)):correspond à la ligne appelé dans le dataframe
>                                     à chaque fois c'est une série de 3 colonnes qui est appelé 
> 
> 
> Returns:
>     series: meme chose que radlon mais degres

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
> Prédit la vitesse des stations GNSS à partir d'un modèle
> (rotation + translation), puis convertit la vitesse du repère ECEF (XYZ)
> vers le repère local ENU (East, North, Up).
> 
> Le modèle utilisé est :
>     v_xyz = ω x r + T
> où :
>   - r = (X, Y, Z) est la position ECEF de la station (m),
>   - ω = (Ωx, Ωy, Ωz) est le vecteur de rotation de la plaque (mas/yr),
>   - T est un terme de translation (m/yr),
>   - v_xyz est la vitesse prédite en ECEF (m/yr).
> 
> La conversion en ENU est faite au point de la station (défini par sa
> longitude λ et latitude φ, obtenues via part1.xyz_to_pol(X, Y, Z),
> Parameters
> ----------
> pmm : pandas.DataFrame
>     Table des paramètres de plaques. Doit contenir au minimum :
>       - 'Name' : identifiant de plaque (clé de jointure)
>       - 'Omega_x', 'Omega_y', 'Omega_z' : composantes de ω en mas/yr
> 
>     Hypothèse : une seule ligne par plaque (sinon la jointure doit échouer
>     avec `validate="m:1"`).
> 
> ITRF : pandas.DataFrame
>     Table des stations. Doit contenir au minimum :
>       - 'Plate' : identifiant de plaque associée à la station
>       - 'X/Vx', 'Y/Vy', 'Z/Vz' : coordonnées ECEF de la station (m)
> 
> Returns
> -------
> ITRFcop : pandas.DataFrame
>     Copie de ITRF  avec :
>       - 'VE', 'VN', 'VU' : composantes de la vitesse prédite en ENU (m/yr)
> 
>     La fonction ne conserve pas explicitement les composantes ECEF dans des
>     colonnes (Vx_pred, Vy_pred, Vz_pred), mais elles sont calculées en
>     interne.     

### Fonction : `incertitude_vitesse`
> _summary_
>   Calcule les incertitudes-type (écarts-types, 1σ) des composantes de vitesse
>   prédite en repère cartésien ECEF (Vx, Vy, Vz), par propagation d'incertitudes
>   en supposant toutes les variables indépendantes.
> 
> - Vx = Wy*Z - Wz*Y + Tx
> - Vy = Wz*X - Wx*Z + Ty
> - Vz = Wx*Y - Wy*X + Tz
> 
>   Propagation d'incertitudes (indépendance)
>   -----------------------------------------
>   On utilise la règle (approximation au 1er ordre) :
>     s(a*b) ≈ sqrt ( b² * s(a)² + a² s(b)²
>     et on peut simplement sommet dans l'incertitude de gauche
> 
>   Args:
> pmm : pandas.DataFrame
>         DataFrame des paramètres de plaques. Doit contenir au minimum :
>           - 'Name' : identifiant de plaque (clé de jointure)
>           - 'Omega_x', 'Omega_y', 'Omega_z' : composantes de ω (mas/yr)
>           - 's_Omega_x', 's_Omega_y', 's_Omega_z' : incertitudes-type sur ω (mas/yr)
> 
>         Hypothèse : une ligne par plaque (contrôlée par validate="m:1").
> 
>     ITRF : pandas.DataFrame
>         DataFrame des stations. Doit contenir au minimum :
>           - 'Plate' : identifiant de plaque associée à la station
>           - 'X/Vx', 'Y/Vy', 'Z/Vz' : coordonnées ECEF de la station (m)
>           - 'Sigma_x', 'Sigma_y', 'Sigma_z' : incertitudes-type sur X,Y,Z (m)
> 
>   Returns
>   -------
>   ITRF_cop : pandas.DataFrame
>       Copie de `TRF enrichie avec les colonnes :
>         -'sigma_Vx,' 'sigma_Vy', 'sigma_Vz' : incertitudes-type sur les composantes de vitesse ECEF (m/yr).
> 
>   

### Fonction : `norme_v`
> _summary_
> permet de retourner la norne d'un tableau numpy en entrer de taille n,3 (vecteurs de 3 dimension)
>   Args:
>       v (np.arrray): tableau rassemblant des vecteurs 3D vitesses
> 
>   Returns:
>       np.arry : tableau  n,1 des normes des vecteurs
>   

### Fonction : `z_score`
> _summary_
> Calcule un z-score de cohérence entre une vitesse qui est donné  dans ITRF2020 et une
> vitesse "calculée/prédite", en comparant leurs normes et en combinant leurs incertitudes-type (1σ).
> Pour information un z-score qui validerai nos calculs doit être inférieur à 2. 
> rappel calcul : 
> z = abs( ||v_cal|| - ||v_obs|| ) / s
> avec l'incertitude combiné :  s = sqrt( s_obs^2 + s_cal^2 )
> Args:
>     calcule : pandas.DataFrame
>     DataFrame contenant les vitesses "calculées" en ECEF et leurs incertitudes
>     sur composantes. Doit contenir au minimum :
>       - 'DOMES NB' : identifiant station (clé de jointure)
>       - 'Vx', 'Vy', 'Vz' : composantes ECEF de vitesse calculée
>       - 'sigma_Vx', 'sigma_Vy', 'sigma_Vz' : incertitudes-type sur Vx,Vy,Vz
>       - 'Norme_ITRF' : norme de la vitesse calculée (||v_cal||)
> 
> donne : pandas.DataFrame
>     DataFrame contenant les vitesses "observées" (ou provenant d'un autre
>     jeu de données) et leurs incertitudes sur composantes. Doit contenir au
>     minimum :
>       - 'DOMES NB' : identifiant station (clé de jointure)
>       - 'X/Vx_vitesse', 'Y/Vy_vitesse', 'Z/Vz_vitesse' : composantes ECEF observées
>       - 'Sigma_x_vitesse', 'Sigma_y_vitesse', 'Sigma_z_vitesse' : incertitudes-type
>       - 'Norme_vitesse' : norme observée (||v_obs||)
>       - 'in_deformation' : indicateur/flag (renvoyé tel quel)
> 
> 
> Returns:
>     _type_: _description_

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

