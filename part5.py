import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import numpy as np


def carte_monde_statique(dico_plaques, df_stations, df_GSRM):
    """
    Génération d'une image d'une carte statique du monde avec Matplotlib 

    Args:
        dico_plaques (dico): Dictionnaire de DataFrames représentant les polygones des plaques.
        df_stations (pd.dataframe): DataFrame contenant les points avec les colonnes 'lon(degres)' et 'lat(degres) des stations GNSS'.
        df_GSRM (pd.dataframe): DataFrame contenant les points avec les colonnes 'lon(degres)' et 'lat(degres) des points de deformation'.
    """
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
    
    ax.stock_img()
    
    ax.add_feature(cfeature.COASTLINE, linewidth=0.5)
    ax.add_feature(cfeature.BORDERS, linestyle=':', alpha=0.5)
    ax.add_feature(cfeature.LAND, facecolor='lightgray', alpha=0.3)
    ax.add_feature(cfeature.OCEAN, facecolor='azure', alpha=0.3)


    colors = plt.cm.tab20.colors 
    
    scatter = ax.scatter(df_GSRM['long'], df_GSRM['lat'],
                            transform=ccrs.PlateCarree(),
                            color='orange', 
                            s=15,  
                            marker='o',
                            label='Deformation',
                            zorder=3,
                            alpha=0.5) 
    
    scatter = ax.scatter(df_stations['lon(degres)'].where(df_stations['Plate'] != 'Unknown'), df_stations['lat(degres)'].where(df_stations['Plate'] != 'Unknown'),
                          transform=ccrs.PlateCarree(),
                          color='red', 
                          s=15,  
                          marker='o',
                          label='Stations GNSS',
                          zorder=10) 
    
    scatter = ax.scatter(df_stations['lon(degres)'].where(df_stations['Plate'] == 'Unknown'), df_stations['lat(degres)'].where(df_stations['Plate'] == 'Unknown'),
                          transform=ccrs.PlateCarree(),
                          color='purple', 
                          s=15,  
                          marker='*',
                          label='Stations GNSS sans plques',
                          zorder=10)  
    
    for i, (nom_plaque, df_plaque) in enumerate(dico_plaques.items()):
        color = colors[i % len(colors)]
        ax.plot(df_plaque['Lon'], df_plaque['Lat'], 
                transform=ccrs.PlateCarree(), 
                label=nom_plaque, 
                color=color, 
                linewidth=1.5,
                zorder=5)

    SCALE_FACTOR = 0.15
    
    mask = df_stations['in_deformation'] == False
    
    q = ax.quiver(df_stations.loc[mask, 'lon(degres)'].values, df_stations.loc[mask,'lat(degres)'].values,
                  df_stations.loc[mask,'VE'].values, df_stations.loc[mask,'VN'].values,
                  transform=ccrs.PlateCarree(),
                  color='darkblue',        
                  width=0.002,           
                  headwidth=2,         
                  headlength=2,            
                  scale=SCALE_FACTOR,      
                  scale_units='inches',   
                  zorder=15,               
                  label='Vitesse prédite')
    
    mask2 = df_stations['in_deformation'] == True
    
    q2 = ax.quiver(df_stations.loc[mask2, 'lon(degres)'].values, df_stations.loc[mask2,'lat(degres)'].values,
                  df_stations.loc[mask2,'VE'].values, df_stations.loc[mask2,'VN'].values,
                  transform=ccrs.PlateCarree(),
                  color='green',        
                  width=0.002,           
                  headwidth=2,         
                  headlength=2,            
                  scale=SCALE_FACTOR,      
                  scale_units='inches',   
                  zorder=15,               
                  label='Vitesse prédite')
    
    REF_VELOCITY = 0.05
    
    ax.quiverkey(q, 
                 X=0.9, Y=0.05,            
                 U=REF_VELOCITY,           
                 label=f'{REF_VELOCITY} m/an', 
                 labelpos='E',             
                 coordinates='axes', fontproperties={'size': 10})

    ax.set_title("Plaques Tectoniques et Stations GNSS")

    plt.style.use('seaborn-v0_8-whitegrid')
    
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05), ncol=5, fontsize='x-small')

    print("Carte générée.")
    plt.savefig("output/Carte_Monde.png",dpi=300, format="png", bbox_inches='tight')

def carte_eurasie_statique(dico_plaques, df_stations, df_GSRM):
    """
    Génération d'une image d'une carte statique de l'eurasie avec Matplotlib 

    Args:
        dico_plaques (dico): Dictionnaire de DataFrames représentant les polygones des plaques.
        df_stations (pd.dataframe): DataFrame contenant les points avec les colonnes 'lon(degres)' et 'lat(degres) des stations GNSS'.
        df_GSRM (pd.dataframe): DataFrame contenant les points avec les colonnes 'lon(degres)' et 'lat(degres) des points de deformation'.
    """
    fig = plt.figure(figsize=(14, 8))
    
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
    
    ax.stock_img()
    
    ax.set_extent([-30, 150, 10, 87], crs=ccrs.PlateCarree())
 
    ax.add_feature(cfeature.COASTLINE, linewidth=0.5)
    ax.add_feature(cfeature.BORDERS, linestyle=':', alpha=0.5)
    ax.add_feature(cfeature.LAND, facecolor='lightgray', alpha=0.3)
    ax.add_feature(cfeature.OCEAN, facecolor='azure', alpha=0.3)

    colors = plt.cm.tab20.colors 
    
    plaque_found = False

    scatter = ax.scatter(df_GSRM['long'], df_GSRM['lat'],
                            transform=ccrs.PlateCarree(),
                            color='orange', 
                            s=15,  
                            marker='o',
                            label='Deformation',
                            zorder=3,
                            alpha=0.5) 

    for i, (nom_plaque, df_plaque) in enumerate(dico_plaques.items()):
        color = colors[i % len(colors)]
        
        linewidth = 1.5
        alpha = 1.0
    

        ax.plot(df_plaque['Lon'], df_plaque['Lat'], 
                transform=ccrs.PlateCarree(), 
                label=nom_plaque, 
                color=color, 
                alpha=alpha,
                linewidth=linewidth,
                zorder=5)

    scatter = ax.scatter(df_stations['lon(degres)'].where(df_stations['Plate'] != 'Unknown'), df_stations['lat(degres)'].where(df_stations['Plate'] != 'Unknown'),
                          transform=ccrs.PlateCarree(),
                          color='red', 
                          s=15,  
                          marker='o',
                          label='Stations GNSS',
                          zorder=10) 
    
    scatter = ax.scatter(df_stations['lon(degres)'].where(df_stations['Plate'] == 'Unknown'), df_stations['lat(degres)'].where(df_stations['Plate'] == 'Unknown'),
                          transform=ccrs.PlateCarree(),
                          color='purple', 
                          s=15,  
                          marker='*',
                          label='Stations GNSS sans plques',
                          zorder=10) 
    
    SCALE_FACTOR = 0.15
    
    mask = df_stations['in_deformation'] == False
    
    q = ax.quiver(df_stations.loc[mask, 'lon(degres)'].values, df_stations.loc[mask,'lat(degres)'].values,
                  df_stations.loc[mask,'VE'].values, df_stations.loc[mask,'VN'].values,
                  transform=ccrs.PlateCarree(),
                  color='darkblue',        
                  width=0.002,           
                  headwidth=2,         
                  headlength=2,            
                  scale=SCALE_FACTOR,      
                  scale_units='inches',   
                  zorder=15,               
                  label='Vitesse prédite')
    
    mask2 = df_stations['in_deformation'] == True
    
    q2 = ax.quiver(df_stations.loc[mask2, 'lon(degres)'].values, df_stations.loc[mask2,'lat(degres)'].values,
                  df_stations.loc[mask2,'VE'].values, df_stations.loc[mask2,'VN'].values,
                  transform=ccrs.PlateCarree(),
                  color='green',        
                  width=0.002,           
                  headwidth=2,         
                  headlength=2,            
                  scale=SCALE_FACTOR,      
                  scale_units='inches',   
                  zorder=15,               
                  label='Vitesse prédite')
    REF_VELOCITY = 0.05 
    
    ax.quiverkey(q, 
                 X=0.9, Y=0.05,           
                 U=REF_VELOCITY,          
                 label=f'{REF_VELOCITY} cm/an',
                 labelpos='E',             
                 coordinates='axes', fontproperties={'size': 10})
    

    ax.set_title("Focus : Plaque Eurasie et Stations GNSS")

    plt.style.use('seaborn-v0_8-whitegrid')
    
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05), ncol=5, fontsize='x-small')

    print("Carte Eurasie générée.")
    plt.savefig("output/Carte_Eurasie.png",dpi=300, format="png", bbox_inches='tight') 