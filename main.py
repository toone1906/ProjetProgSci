import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from tqdm import tqdm 
import time
import json
import part1
import part2
import part3
import part4
import part5


if __name__ == "__main__":

    tqdm.pandas(desc="Calcul coordonnées")

    d1 = time.time()

    print("--- Démarrage du chargement des données ---")
    with tqdm(total=3, desc="Chargement fichiers") as pbar:
        
        colspecs_ITRF = [(0, 9),(10, 25), (26,30),(32, 36),(37, 50),(51, 64),(65, 79),(79, 85),(86, 92),(93, 99),(100, 102),(103, 115),(116, 128)]
        ITRF_2020 = pd.read_fwf("data/ITRF2020_GNSS.SSC.txt", skiprows=8,colspecs=colspecs_ITRF, names=["DOMES NB", "SITE NAME", "TECH","ID", "X/Vx","Y/Vy","Z/Vz","Sigma_x","Sigma_y","Sigma_z","SOLN","DATA_START","DATA_END"] )
        pmm_itrf = pd.read_csv("data/pmm_itrf.txt",sep=r'\s+',skiprows=4,names=["Plate", "Name", "NS","Omega_x", "Omega_y","Omega_z","Omega","WRMS_E","WRMS_N","s_Omega_x","s_Omega_y","s_Omega_z","s_Omega"],engine='c')
        pbar.update(1)
        
        with open("data/Tectonic_Plates.geojson") as f:
            Plaques_Techtoniques = json.load(f)
        pbar.update(1)
        
        GSRM = pd.read_csv("data/GSRM_strain.txt",skiprows=25,sep=r'\s+',names=["lat","long", "exx","eyy","exy","vorticity","RL-NLC","LL-NLC","e1","e2","azi_e1"],engine='c' )
        pbar.update(1)

        d2 = time.time()
        tqdm.write(f'Ouverture fichiers terminée en {d2-d1:.2f}s')

        last_version_position2 = ITRF_2020.loc[(ITRF_2020['SITE NAME'].notna())]
        last_version_position2 = last_version_position2.drop_duplicates(subset= 'SITE NAME', keep = 'last' )

        tmp = ITRF_2020.copy()
        tmp['DOMES_base'] = tmp['DOMES NB'].str[:-4]

        last_version_vitesse = tmp.drop_duplicates(subset='DOMES_base',keep='last').drop(columns='DOMES_base')

        last_version_vitesse = last_version_vitesse.loc[:, ['DOMES NB', 'X/Vx', 'Y/Vy','Z/Vz','Sigma_x','Sigma_y','Sigma_z']]
        #1.1.3 : Conversion cartésien -> lat/lon
        print("\nConversion des coordonnées")

        last_version_position2['lon(rad)'] = last_version_position2.progress_apply(part1.radlon, axis = 1)
        last_version_position2['lat(rad)'] = last_version_position2.progress_apply(part1.radlat, axis = 1)
        last_version_position2['lon(degres)'] = last_version_position2.progress_apply(part1.degreslon, axis = 1 )
        last_version_position2['lat(degres)'] = last_version_position2.progress_apply(part1.degreslat, axis = 1)

        GSRM["deformation"] = np.sqrt(GSRM["exx"]**2 + GSRM["eyy"]**2 + 2 * GSRM["exy"]**2)
        GSRM = GSRM[GSRM["deformation"] > 50]
        GSRM = GSRM.sort_values(by=["lat", "long", "deformation"], ascending=True)
        GSRM = GSRM.drop_duplicates(subset=["lat","long"], keep="last")

        # 1.3
        dico_plaques = {}
        features_list = Plaques_Techtoniques["features"]

        for feature in tqdm(features_list, desc="Analyse géométrie plaques"):
            nom = feature["properties"]["PlateName"]
            coords = feature["geometry"]["coordinates"]
            type_geom = feature["geometry"]["type"] # renommé 'type' en 'type_geom' pour éviter conflit mot-clé python
            
            points = []
            if type_geom == "Polygon":
                points = coords[0]
            elif type_geom == "MultiPolygon":
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
            
        pmm_itrf["Name"] = pmm_itrf["Name"].str.replace("_", " ")
                
        noms_itrf = set(pmm_itrf["Name"].unique())

        dico_plaques_pmm_noms = {
            nom: df 
            for nom, df in dico_plaques.items() 
            if nom in noms_itrf
        }

        #2
        print("\nCalculs d'appartenance aux plaques...")
        with tqdm(total=2, desc="Calculs spatiaux (Part 2)") as pbar:

            gdf_joined = part2.isIn_geoPandas(last_version_position2, "data/Tectonic_Plates.geojson")
            test_version = last_version_position2.copy()
            test_version['Plate'] = gdf_joined['PlateName']
            pbar.update(1)
            
            last_version_position2['Plate'] = part2.isIn_mat(last_version_position2, dico_plaques_pmm_noms)
            pbar.update(1)

        print("Affichage des stations avec leur plaque tectonique associée (échantillon) :")

        #3
        d = time.time()
        print("\nRecherche de déformation la plus proche...")

        with tqdm(total=1, desc="Calcul Proximité (Part 3)") as pbar:
            res_proxi = part3.proxi(GSRM, last_version_position2)
            pbar.update(1)


        d1 = time.time()
        print(f'Temps calcul déformation : {d1-d:.2f}s')

    #4

    incertitude_proxi = part4.incertitude_vitesse(pmm_itrf,res_proxi) # incertitude ajouter
    res_proxi = part4.v_pred(pmm_itrf,incertitude_proxi)


    

        #5
    print("\nGénération des cartes...\n")

    part5.carte_monde_statique(dico_plaques_pmm_noms, res_proxi, GSRM)
    part5.carte_eurasie_statique(dico_plaques_pmm_noms, res_proxi, GSRM)

        #Comparaisons de données
    #last_version_vitesse['Norme'] = np.sqrt((last_version_vitesse['X/Vx']**2 + last_version_vitesse['Y/Vy']**2 +last_version_vitesse['Z/Vz']**2))
    res_proxi['Norme'] = part4.norme_v(res_proxi[["Vx", "Vy", "Vz"]].to_numpy() )
    last_version_vitesse['Norme'] = part4.norme_v(last_version_vitesse[["X/Vx", "Y/Vy", "Z/Vz"]].to_numpy() )

    # Création du dataframe avec la moyenne des normes par plaques
    df_moyenne_normes = res_proxi.groupby('Plate')['Norme'].mean().reset_index(name='Moyenne_Norme').sort_values(by=['Moyenne_Norme'], ascending=False)
    print("\nMoyenne des normes par plaques :")
    print(df_moyenne_normes)

    last_version_vitesse = last_version_vitesse.sort_values(by=['Norme'], ascending=False)
    res_proxi = res_proxi.sort_values(by=['Norme'], ascending=False)

    print("\n10 plus grands déplacement pour des stations \n")
    print("Données de base : \n")
    print(last_version_vitesse.head(10))
    print("\nCalculés : \n")
    print(res_proxi[['DOMES NB', 'Vx', 'Vy', 'Vz', 'Norme']].head(10))

    last_version_vitesse = last_version_vitesse.sort_values(by=['Norme'], ascending=True)
    res_proxi = res_proxi.sort_values(by=['Norme'], ascending=True)

    print("\n10 plus petits déplacement pour des stations \n")
    print("Données de base : \n")
    print(last_version_vitesse.head(10))
    print("\nCalculés : \n")
    print(res_proxi[['DOMES NB', 'Vx', 'Vy', 'Vz', 'Norme']].head(10))
    
    conclusion = part4.z_score(res_proxi,last_version_vitesse)
    #suppression des stations sur plaque inconnu 
    conclusion = conclusion.loc[conclusion["z_score"].notna()]
    conclusion_decroiss = conclusion.sort_values(by=['z_score'], ascending=False)
    conclusion_croiss =  conclusion.sort_values(by=['z_score'], ascending=True)
    print("15 plus petit z-score  \n")
    print(conclusion_croiss.head(10))
    print("\n 15 plus grand z-score  \n")
    print(conclusion_decroiss.head(10))
    
    print("\nZ Score moyen  \n")
    print(np.mean(conclusion["z_score"]))
    print(np.median(conclusion["z_score"]))

    print("\nZ Score moyen  hors zones de deformations\n")
    print(np.mean(conclusion["z_score" ].where(conclusion['in_deformation']==False)))
    print("z_score très légérement supérieur à 2, on peut difficlement conclure sur \n la vitesse des stations dans les zones de non déformation")
    conclusion[["SITE NAME","z_score","in_deformation"]].to_csv("tableau_z_score.csv")
    

    print("\n--- Terminée ---")