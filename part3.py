import pandas as pd 
import math as m 
import numpy as np 

def distance_haversine(phi1,phi2,lambda1,lambda2): 
    Rt = 6378E3
    return 2*Rt*m.asin(m.sqrt(m.sin((phi2-phi1)/2)**2+ m.cos(phi1)*m.cos(phi2)*m.sin((lambda2 - lambda1)/2)**2)))



GSRM = pd.read_fwf("data/GSRM_strain.txt", skiprows=25,  names=["lat","long", "exx","eyy","exy","vorticity","RL-NLC","LL-NLC","e1","e2","azi_e1"] )

GSRM["deformation"] = np.sqrt(GSRM["exx"]**2 + GSRM["eyy"]**2 + 2 * GSRM["exy"]**2)

forte_deformation = GSRM[GSRM["deformation"] > 50]

forte_deformation = forte_deformation.sort_values(by=["lat", "long", "deformation"], ascending=True)

# forte_deformation_sans_doublons = forte_deformation.drop_duplicates(subset=["lat","long"], keep="last")