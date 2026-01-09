import pandas as pd 


T = (0.37,0.35,0.74)
sT = (0.08,0.10,0.09)

def v_pred(ppm,ITRF):
    ITRF['V_pred'] = ITRF['Plate']





pmm_itrf = pd.read_csv("data/pmm_itrf.txt",sep='\s+',skiprows=4,names=["Plate", "Name", "NS","Omega_x", "Omega_y","Omega_z","Omega","WRMS","Sigma_y","s_Omega_x","s_Omega_y","s_Omega_z","s_Omega"])
print(pmm_itrf)



