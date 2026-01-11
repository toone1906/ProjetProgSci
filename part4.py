import pandas as pd 
import numpy as np
import part1

T = (0.37,0.35,0.74)
sT = (0.08,0.10,0.09)

def v_pred(pmm,ITRF):
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
    ITRFcop[["VE","VN","VU"]] = VENU

    return ITRFcop