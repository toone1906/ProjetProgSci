import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature


def afficher_carte_interactive(dico_plaques, df_stations):
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
    
    ax.add_feature(cfeature.COASTLINE, linewidth=0.5)
    ax.add_feature(cfeature.BORDERS, linestyle=':', alpha=0.5)
    ax.add_feature(cfeature.LAND, facecolor='lightgray', alpha=0.3)
    ax.add_feature(cfeature.OCEAN, facecolor='azure', alpha=0.3)


    colors = plt.cm.tab20.colors 
    
    for i, (nom_plaque, df_plaque) in enumerate(dico_plaques.items()):
        color = colors[i % len(colors)]
        ax.plot(df_plaque['Lon'], df_plaque['Lat'], 
                transform=ccrs.PlateCarree(), 
                label=nom_plaque, 
                color=color, 
                linewidth=1.5)


    scatter = ax.scatter(df_stations['lon(degres)'], df_stations['lat(degres)'],
                         transform=ccrs.PlateCarree(),
                         color='red', 
                         s=10, 
                         marker='o',
                         label='Stations GNSS',
                         zorder=5) 

    ax.set_title("Plaques Tectoniques et Stations GNSS")

    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05), ncol=5, fontsize='x-small')

    print("Carte générée. Utilisez les outils de la fenêtre pour zoomer/déplacer.")
    plt.show()

