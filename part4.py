import pandas as pd 
import numpy as np

T = (0.37,0.35,0.74)
sT = (0.08,0.10,0.09)

def v_pred(pmm,ITRF):
    ITRFcop = ITRF.copy()
    merge_ITRF = ITRFcop.merge(pmm[["Name","Omega_x","Omega_y","Omega_z"]],left_on = "Plate", right_on = "Name", how = "left",validate="m:1")
    wx,wy,wz = merge_ITRF["Omega_x"].to_numpy() ,merge_ITRF["Omega_y"].to_numpy(), merge_ITRF["Omega_z"].to_numpy()
    omega = np.column_stack((wx,wy,wz)) # en mas/yr
    X,Y,Z = merge_ITRF["X/Vx"].to_numpy(), merge_ITRF["Y/Vy"].to_numpy(), merge_ITRF["Z/Vz"].to_numpy()
    coord = np.column_stack((X,Y,Z))
    T = np.array([0.37,0.35,0.74]) * 0.001 # m/yr
    MAS_TO_RAD = np.deg2rad(1/3600/1000)  # = 4.848...e-9 rad/mas
    omegarad = omega * MAS_TO_RAD # rad/year
    v = np.cross(omegarad,coord) + T # m/yr
    ITRFcop[["Vx_pred","Vy_pred","Vz_pred"]] = v
    return ITRFcop












#pmm_itrf = pd.read_csv("data/pmm_itrf.txt",sep='\s+',skiprows=4,names=["Plate", "Name", "NS","Omega_x", "Omega_y","Omega_z","Omega","WRMS","Sigma_y","s_Omega_x","s_Omega_y","s_Omega_z","s_Omega"])
#print(pmm_itrf)



