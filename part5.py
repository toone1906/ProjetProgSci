import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import numpy as np


def carte_monde_statique(dico_plaques, df_stations, df_GSRM):
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
    
    ax.add_feature(cfeature.COASTLINE, linewidth=0.5)
    ax.add_feature(cfeature.BORDERS, linestyle=':', alpha=0.5)
    ax.add_feature(cfeature.LAND, facecolor='lightgray', alpha=0.3)
    ax.add_feature(cfeature.OCEAN, facecolor='azure', alpha=0.3)


    colors = plt.cm.tab20.colors 
    

    scatter = ax.scatter(df_GSRM['long'], df_GSRM['lat'],
                          transform=ccrs.PlateCarree(),
                          color='orange', 
                          s=15,  # Points légèrement plus gros pour la vue zoomée
                          marker='o',
                          label='Deformation',
                          zorder=3,
                          alpha=0.5) 

    scatter = ax.scatter(df_stations['lon(degres)'], df_stations['lat(degres)'],
                         transform=ccrs.PlateCarree(),
                         color='red', 
                         s=10, 
                         marker='o',
                         label='Stations GNSS',
                         zorder=10) 
    
    for i, (nom_plaque, df_plaque) in enumerate(dico_plaques.items()):
        color = colors[i % len(colors)]
        ax.plot(df_plaque['Lon'], df_plaque['Lat'], 
                transform=ccrs.PlateCarree(), 
                label=nom_plaque, 
                color=color, 
                linewidth=1.5,
                zorder=5)

    ax.set_title("Plaques Tectoniques et Stations GNSS")

    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05), ncol=5, fontsize='x-small')

    print("Carte générée. Utilisez les outils de la fenêtre pour zoomer/déplacer.")
    plt.savefig("Carte_monde.png", format="png")
    plt.show()

import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

def carte_eurasie_statique(dico_plaques, df_stations, df_GSRM):
    fig = plt.figure(figsize=(14, 8))
    
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
    
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
                            s=15,  # Points légèrement plus gros pour la vue zoomée
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

    scatter = ax.scatter(df_stations['lon(degres)'], df_stations['lat(degres)'],
                          transform=ccrs.PlateCarree(),
                          color='red', 
                          s=15,  # Points légèrement plus gros pour la vue zoomée
                          marker='o',
                          label='Stations GNSS',
                          zorder=10) 
    SCALE_FACTOR = 0.05
    
    q = ax.quiver(df_stations['lon(degres)'].values, df_stations['lat(degres)'].values,
                  df_stations['Vx_pred'].values, df_stations['Vy_pred'].values,
                  transform=ccrs.PlateCarree(),
                  color='darkblue',        # Couleur des flèches
                  width=0.002,             # Épaisseur du corps de la flèche
                  headwidth=3,             # Largeur de la tête
                  headlength=4,            # Longueur de la tête
                  scale=SCALE_FACTOR,      # L'échelle (le plus important !)
                  scale_units='inches',    # Unité de l'échelle pour rester cohérent au zoom
                  zorder=15,               # Tout en haut
                  label='Vitesse prédite')
    REF_VELOCITY = 50 # La valeur de la flèche de référence (ex: 50 mm/an)
    
    ax.quiverkey(q, 
                 X=0.9, Y=0.05,            # Position de la légende (en bas à droite)
                 U=REF_VELOCITY,           # Longueur de la flèche de référence
                 label=f'{REF_VELOCITY} mm/an', # Texte de la légende
                 labelpos='E',             # Texte à l'Est de la flèche
                 coordinates='axes', fontproperties={'size': 10})
    

    ax.set_title("Focus : Plaque Eurasie et Stations GNSS")

    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05), ncol=5, fontsize='x-small')

    print("Carte Eurasie générée.")
    plt.savefig("Carte_Eurasie.png", format="png", bbox_inches='tight') 
    plt.show()
