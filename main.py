import numpy as np
import pandas as pd 
import matplotlib as plt
import cartopy 
import datetime
import tqdm

earth = pd.read_fwf("data/Earth_Parameters.dat", skiprows = 8)


GSRM = pd.read_fwf("data/GSRM_strain.txt", skiprows=25,  names=["lat","long", "exx","eyy","exy","vorticity","RL-NLC","LL-NLC","e1","e2","azi_e1"] )
ITRF_2020 = pd.read_fwf("data/ITRF2020_GNSS.SSC.txt", skiprows=8,  names=["DOMES NB", "SITE NAME", "TECH","ID", "X/Vx","Y/Vy","Z/Vz","Sigma_x","Sigma_y","Sigma_z","SOLN","DATA_START","DATA_END"] )
pmm_itrf = pd.read_csv("data/pmm_itrf.txt",sep='\s+',skiprows=4,names=["Plate", "Name", "NS","Omega_x", "Omega_y","Omega_z","Omega","WRMS","Sigma_y","s_Omega_x","s_Omega_y","s_Omega_z","s_Omega"])

GSRM["deformation"] = np.sqrt(GSRM["exx"]**2 + GSRM["eyy"]**2 + 2 * GSRM["exy"]**2)

forte_deformation = GSRM[GSRM["deformation"] > 50]

forte_deformation = forte_deformation.sort_values(by=["lat", "long", "deformation"], ascending=True)

forte_deformation_sans_doublons = forte_deformation.drop_duplicates(subset=["lat","long"], keep="last")
