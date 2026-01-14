import pandas as pd 
import numpy as np
import part1

T = (0.37,0.35,0.74)
sT = (0.08,0.10,0.09)

def v_pred(pmm,ITRF):
    '''
    Calcul la vitesse des stations GNSS à partir d'un modèle, puis convertit 
    la vitesse du repère ECEF (XYZ) vers le repère local ENU (East, North, Up).
    Indispensable pour projeter les vecteurs sur la carte de cartopy.

    Le modèle vectoriel utilisé est :
        v_xyz = ω x r + T
    où :
      - r = (X, Y, Z) est la position ECEF de la station (m),
      - ω = (Ωx, Ωy, Ωz) est le vecteur de rotation de la plaque (mas/yr),
      - T est une constante terrestre de translation (m/yr),
      - v_xyz est la vitesse prédite en ECEF (m/yr).

    La conversion en ENU est faite au point de la station (défini par sa
    longitude λ et latitude φ, obtenues via `part1.xyz_to_pol(X, Y, Z)`),
    par une rotation orthonormée (la norme de la vitesse est conservée).

    :param: 
    pmm : pandas.DataFrame
        Table des paramètres de plaques. Contient en particulier:
          - 'Name' : identifiant de plaque (clé de jointure)
          - 'Omega_x', 'Omega_y', 'Omega_z' : composantes de ω en mas/yr

        

    ITRF : pandas.DataFrame
        Table des stations. Contient en particulier :
          - 'Plate' : identifiant de plaque associée à la station
          - 'X/Vx', 'Y/Vy', 'Z/Vz' : coordonnées ECEF de la station (m)
    
          Hypothèse : une seule plaque par station, soit plusieurs station sur une meme plaque 
          mais pas l'inverse, échoue alors avec `validate="m:1"`

    Returns
    -------
    ITRFcop : pandas.DataFrame
        Copie de `ITRF` enrichie avec :
          - 'VE', 'VN', 'VU' : composantes de la vitesse prédite en ENU (m/yr)

        La fonction ne conserve pas explicitement les composantes ECEF dans des
        colonnes (Vx_pred, Vy_pred, Vz_pred), mais elles sont calculées en
        interne.
        Valeurs parfaitement inutile 

    Cependant à utiliser plus tard en vue d'un z_score.
    '''
    ITRFcop = ITRF.copy()
    merge_ITRF = ITRFcop.merge(pmm[["Name","Omega_x","Omega_y","Omega_z"]],left_on = "Plate", right_on = "Name", how = "left",validate="m:1")
    omega = merge_ITRF[["Omega_x","Omega_y","Omega_z"]].to_numpy() # en mas/yr
    coord = merge_ITRF[["X/Vx","Y/Vy","Z/Vz"]].to_numpy()
    T = np.array([0.37,0.35,0.74]) * 0.001 # m/yr
    MAS_TO_RAD = np.deg2rad(1/3600/1000)  # = 4.848...e-9 rad/mas
    omegarad = omega * MAS_TO_RAD # rad/year
    v = np.cross(omegarad,coord) + T # m/yr
    Vx,Vy,Vz = v[:,0],v[:,1],v[:,2]
    X,Y,Z = coord[:,0], coord[:,1],coord[:,2]
    vlamb, vphi = part1.xyz_to_pol(X,Y,Z) #position des vecteurs vitesse sur la carte
    sinphi, cosphi = np.sin(vphi), np.cos(vphi)
    sinlamb, coslamb = np.sin(vlamb), np.cos(vlamb)
    Ve = -sinlamb*Vx + coslamb*Vy # formation des vecteurs en ENU qui conserve la norme 
    Vn =  -sinphi*coslamb*Vx + -sinphi*sinlamb*Vy + cosphi*Vz
    Vu =  cosphi*coslamb*Vx + cosphi*sinlamb*Vy + sinphi*Vz 
    VENU = np.column_stack((Ve,Vn,Vu))
    ITRFcop[["Vx","Vy","Vz"]] = v
    ITRFcop[["VE","VN","VU"]] = VENU

    return ITRFcop