import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature


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
                          zorder=5) 

    scatter = ax.scatter(df_stations['lon(degres)'], df_stations['lat(degres)'],
                         transform=ccrs.PlateCarree(),
                         color='red', 
                         s=10, 
                         marker='o',
                         label='Stations GNSS',
                         zorder=5) 
    
    for i, (nom_plaque, df_plaque) in enumerate(dico_plaques.items()):
        color = colors[i % len(colors)]
        ax.plot(df_plaque['Lon'], df_plaque['Lat'], 
                transform=ccrs.PlateCarree(), 
                label=nom_plaque, 
                color=color, 
                linewidth=1.5)

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
                            zorder=5) 

    for i, (nom_plaque, df_plaque) in enumerate(dico_plaques.items()):
        color = colors[i % len(colors)]
        
        linewidth = 1.5
        alpha = 1.0
    

        ax.plot(df_plaque['Lon'], df_plaque['Lat'], 
                transform=ccrs.PlateCarree(), 
                label=nom_plaque, 
                color=color, 
                alpha=alpha,
                linewidth=linewidth)

    scatter = ax.scatter(df_stations['lon(degres)'], df_stations['lat(degres)'],
                          transform=ccrs.PlateCarree(),
                          color='red', 
                          s=15,  # Points légèrement plus gros pour la vue zoomée
                          marker='o',
                          label='Stations GNSS',
                          zorder=5) 
    
    

    ax.set_title("Focus : Plaque Eurasie et Stations GNSS")

    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05), ncol=5, fontsize='x-small')

    print("Carte Eurasie générée.")
    plt.savefig("Carte_Eurasie.png", format="png", bbox_inches='tight') 
    plt.show()
