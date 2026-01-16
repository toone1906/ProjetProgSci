import pandas as pd 
import numpy as np
import part1

T = (0.37,0.35,0.74)
sT = (0.08,0.10,0.09)

def v_pred(pmm, ITRF):
  """
  Prédit la vitesse des stations GNSS à partir d'un modèle
  (rotation + translation), puis convertit la vitesse du repère ECEF (XYZ)
  vers le repère local ENU (East, North, Up).

  Le modèle utilisé est :
      v_xyz = ω x r + T
  où :
    - r = (X, Y, Z) est la position ECEF de la station (m),
    - ω = (Ωx, Ωy, Ωz) est le vecteur de rotation de la plaque (mas/yr),
    - T est un terme de translation (m/yr),
    - v_xyz est la vitesse prédite en ECEF (m/yr).

  La conversion en ENU est faite au point de la station (défini par sa
  longitude λ et latitude φ, obtenues via part1.xyz_to_pol(X, Y, Z),
  Parameters
  ----------
  pmm : pandas.DataFrame
      Table des paramètres de plaques. Doit contenir au minimum :
        - 'Name' : identifiant de plaque (clé de jointure)
        - 'Omega_x', 'Omega_y', 'Omega_z' : composantes de ω en mas/yr

      Hypothèse : une seule ligne par plaque (sinon la jointure doit échouer
      avec `validate="m:1"`).

  ITRF : pandas.DataFrame
      Table des stations. Doit contenir au minimum :
        - 'Plate' : identifiant de plaque associée à la station
        - 'X/Vx', 'Y/Vy', 'Z/Vz' : coordonnées ECEF de la station (m)

  Returns
  -------
  ITRFcop : pandas.DataFrame
      Copie de ITRF  avec :
        - 'VE', 'VN', 'VU' : composantes de la vitesse prédite en ENU (m/yr)

      La fonction ne conserve pas explicitement les composantes ECEF dans des
      colonnes (Vx_pred, Vy_pred, Vz_pred), mais elles sont calculées en
      interne.     
  """
  ITRFcop = ITRF.copy()
  merge_ITRF = ITRFcop.merge(pmm[["Name", "Omega_x", "Omega_y", "Omega_z"]],left_on="Plate",right_on="Name",how="left",validate="m:1")
  omega = merge_ITRF[["Omega_x", "Omega_y", "Omega_z"]].to_numpy()  # mas/yr
  coord = merge_ITRF[["X/Vx", "Y/Vy", "Z/Vz"]].to_numpy()  # m

  T = np.array([0.37, 0.35, 0.74]) * 0.001  # m/yr (à partir de mm/yr)
  MAS_TO_RAD = np.deg2rad(1 / 3600 / 1000)  # rad/mas
  omegarad = omega * MAS_TO_RAD  # rad/yr

  v = np.cross(omegarad, coord) + T  # m/yr
  Vx, Vy, Vz = v[:, 0], v[:, 1], v[:, 2]

  X, Y, Z = coord[:, 0], coord[:, 1], coord[:, 2]
  vlamb, vphi = part1.xyz_to_pol(X, Y, Z)

  sinphi, cosphi = np.sin(vphi), np.cos(vphi)
  sinlamb, coslamb = np.sin(vlamb), np.cos(vlamb)

  Ve = -sinlamb * Vx + coslamb * Vy
  Vn = -sinphi * coslamb * Vx + -sinphi * sinlamb * Vy + cosphi * Vz
  Vu = cosphi * coslamb * Vx + cosphi * sinlamb * Vy + sinphi * Vz

  VENU = np.column_stack((Ve, Vn, Vu))
  ITRFcop[["Vx", "Vy", "Vz"]] = v
  ITRFcop[["VE", "VN", "VU"]] = VENU
  
  return ITRFcop




def incertitude_vitesse(pmm,ITRF): 
  """_summary_

  Args:
      pmm (_type_): _description_
      ITRF (_type_): _description_
  """
  sT = np.array([0.08,0.35,0.09])* 1E-3 # m/yr
  sTx, sTy, sTz = sT
  MAS_TO_RAD = np.deg2rad(1/3600/1000)  # rad/mas
  ITRF_cop = ITRF.copy()
  merge_ITRF = ITRF_cop.merge(pmm[["Name","Omega_x","Omega_y","Omega_z","s_Omega_x","s_Omega_y","s_Omega_z"]],left_on ="Plate",right_on = "Name",how = "left", validate = "m:1")
  
  
  omega = merge_ITRF[["Omega_x", "Omega_y", "Omega_z"]].to_numpy() * MAS_TO_RAD # mas/yr
  somega = merge_ITRF[["s_Omega_x", "s_Omega_y", "s_Omega_z"]].to_numpy() * MAS_TO_RAD # mas/yr
  Wx, Wy, Wz = omega[:,0],omega[:,1],omega[:,2]
  sWx,sWy,sWz = somega[:,0],somega[:,1],somega[:,2]

  coord = merge_ITRF[["X/Vx", "Y/Vy", "Z/Vz"]].to_numpy()  # m
  scoord = merge_ITRF[["Sigma_x","Sigma_y","Sigma_z"]].to_numpy()  # m
  X,Y,Z = coord[:, 0], coord[:, 1], coord[:, 2]
  sX,sY,sZ = scoord[:, 0], scoord[:, 1], scoord[:, 2]

# propagation incertitude via la variance indépendante (plus simple)

# Vx = Wy*Z - Wz*Y + Tx
  varVx = (Z**2)*(sWy**2) + (Wy**2)*(sZ**2) + (Y**2)*(sWz**2) + (Wz**2)*(sY**2) + (sTx**2)
# Vy = Wz*X - Wx*Z + Ty

  varVy = (X**2)*(sWz**2) + (Wz**2)*(sX**2) + (Z**2)*(sWx**2) + (Wx**2)*(sZ**2) + (sTy**2)

# Vz = Wx*Y - Wy*X + Tz
  varVz = (Y**2)*(sWx**2) + (Wx**2)*(sY**2) + (X**2)*(sWy**2) + (Wy**2)*(sX**2) + (sTz**2)

#calcul incertitude
  sVx = np.sqrt(varVx)
  sVy = np.sqrt(varVy)
  sVz = np.sqrt(varVz)

  sV = np.column_stack((sVx,sVy,sVz))
  ITRF_cop[["sigma_Vx","sigma_Vy","sigma_Vz"]] = sV
  return ITRF_cop



def norme_v (v):       #tableau de dimension 3 en entrer

  Vx, Vy,Vz = v[:,0],v[:,1],v[:,2]
  return np.sqrt(Vx**2+Vy**2+Vz**2)

def z_score(calcule,donne): 
  ITRFcop = calcule.copy()
  mergeITRF = ITRFcop.merge(donne, on = 'DOMES NB', suffixes = ('_ITRF','_vitesse'))

  sVx_vitesse, sVy_vitesse,sVz_vitesse = mergeITRF[['Sigma_x_vitesse','Sigma_y_vitesse','Sigma_z_vitesse']].to_numpy().T
  Vx_vitesse, Vy_vitesse, Vz_vitesse = mergeITRF[['X/Vx_vitesse','Y/Vy_vitesse','Z/Vz_vitesse']].to_numpy().T
  norme_vitesse = mergeITRF['Norme_vitesse'].to_numpy()
  snorme_vitesse = 1/norme_vitesse * np.sqrt((Vx_vitesse**2)*(sVx_vitesse**2) + (Vy_vitesse**2)*(sVy_vitesse**2) + (Vz_vitesse**2)*(sVz_vitesse**2))
  
  norme_recalc = np.sqrt(Vx_vitesse**2 + Vy_vitesse**2 + Vz_vitesse**2)
  ratio = norme_recalc / norme_vitesse
  print("ratio min/med/max:", np.nanmin(ratio), np.nanmedian(ratio), np.nanmax(ratio))

  sVx_calcule, sVy_calcule, sVz_calcule = mergeITRF[['sigma_Vx','sigma_Vy','sigma_Vz']].to_numpy().T
  Vx_calcule, Vy_calcule, Vz_calcule =  mergeITRF[['Vx','Vy', 'Vz']].to_numpy().T
  norme_calcule = mergeITRF['Norme_ITRF'].to_numpy()
  snorme_calcule = 1/norme_calcule *  np.sqrt((Vx_calcule**2)*(sVx_calcule**2) + (Vy_calcule**2)*(sVy_calcule**2) + (Vz_calcule**2)*(sVz_calcule**2))
  print('norme°cal', snorme_calcule,snorme_vitesse)
  snorme = np.sqrt(snorme_vitesse**2 + snorme_calcule**2)
  z_score = abs(norme_calcule-norme_vitesse)/ snorme
  mergeITRF["z_score"] = z_score



  return mergeITRF[["DOMES NB", "Norme_vitesse", "Norme_ITRF","z_score", "in_deformation"]]

