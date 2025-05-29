import pandas as pd
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt
import descartes

import matplotlib.cm as cm
# from matplotlib.scalebar import ScaleBar
from mpl_toolkits.axes_grid1 import make_axes_locatable
from mpl_toolkits.axes_grid1.anchored_artists import AnchoredSizeBar
import matplotlib.gridspec as gridspec
import matplotlib.colors as colors
from mpl_toolkits.axes_grid1.inset_locator import inset_axes




strikes = gpd.read_file("../data/shapefiles/strikes_50ha_UTM_17N.shp")

gapsmax= gpd.read_file('../output/SpatialDistance/gapsmax.shp')

allbufferdf= gpd.read_file('../output/SpatialDistance/allbufferdf.shp')

df_gaps_union= gpd.read_file('../output/SpatialDistance/df_gaps_union.shp')

weightedMean = pd.read_csv('../output/SpatialDistance/stats_weighted_mean_percent_rings.csv')



nameunion = gapsmax.nstrike.values


plt.rcParams['font.family'] = 'Times New Roman'
SMALL_SIZE = 10
MEDIUM_SIZE = 12
BIGGER_SIZE = 12
Legend_size = 16
plt.rc('font', size=12)          # controls default text sizes
plt.rc('axes', titlesize=MEDIUM_SIZE)     # fontsize of the axes title
plt.rc('axes', labelsize=MEDIUM_SIZE)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('legend', fontsize=12)
# fig, ax = plt.subplots(figsize = (4,4))

size=[5.9,9.3]
grid=[5,3]


col=[]
abcd = ["(a)", "(b)" , "(c)" ,"(d)", "(e)", "(f)",
"(g)", "(h)" , "(i)" ,"(j)", "(l)", "(m)",
"(n)", "(o)" , "(p)" ,"(q)", "(r)", "(s)" ]
fig = plt.figure( figsize=(size[0],size[1]) , facecolor='w' )
#########################################################################
# gridspec inside gridspec
outer_grid = gridspec.GridSpec(grid[0], grid[1], wspace=0.1, hspace=0.1)
#########################################################################
### plot each image in subplot
i=0
#Number of lines * number of columns
for i in range(grid[0]*grid[1]):

    #if i is different of the last element
    if i != (grid[0]*grid[1]-1):

        ax = plt.subplot(grid[0], grid[1], i+1)

        ax.set_title('Strike '+nameunion[i])

        selallbufferdf = allbufferdf.loc[allbufferdf.nstrike==nameunion[i],:]
        
        selgapsmax = gapsmax.loc[gapsmax.nstrike==nameunion[i],:]
        
        selstrikes = strikes.loc[strikes.nstrike==nameunion[i],:]

        seluniongapsrings = df_gaps_union.loc[df_gaps_union.nstrike_1==nameunion[i],:]
        
        selallbufferdf.boundary.plot(ax=ax, color='gray', lw=0.8)
        selgapsmax.boundary.plot(ax=ax, color='k', lw=0.5)

        selstrikes.plot(ax=ax, color='k', markersize=10)

        seluniongapsrings.plot(ax=ax, column='percent_ar', cmap='Reds', legend=False, vmin=0, vmax=100, ) #cax=cax)
        
        ax.text(0.05, 1.07, abcd[i], transform=ax.transAxes, size=12)
        ax.set_title('Strike '+nameunion[i])
        
        ax.tick_params(left = False, right = False , labelleft = False ,
                        labelbottom = False, bottom = False)
        
    # this do the last subplot    
    else:

        nameunion = gapsmax.nstrike.values
        print(nameunion)
    

        selallbufferdf = allbufferdf.loc[allbufferdf.nstrike==nameunion[0],:]

        selstrikes = strikes.loc[strikes.nstrike==nameunion[0],:]

        seluniongapsrings = df_gaps_union.groupby('idrings').percent_ar.mean()

        selallbufferdf['mean_per']=seluniongapsrings.values


        #I added this to plot the weighted average
        selallbufferdf['mean_per_2']=weightedMean.area_gap_r.values
        print(weightedMean.area_gap_r)
        print(selallbufferdf)


        list_stat = 'mean_per_2'
        list_title = '   W Mean (%)'

        ax = plt.subplot(grid[0], grid[1], i+1)

        selallbufferdf.plot(ax=ax, column=list_stat ,cmap='jet', legend=True)
    
        selstrikes.plot(ax=ax, color='k', markersize=10)

        selallbufferdf.boundary.plot(ax=ax, color='k', lw=0.8)

        ax.text(0.05, 1.07, abcd[i], transform=ax.transAxes, size=12)

        ax.set_title(list_title)

        ax.tick_params(left = False, right = False , labelleft = False,
            labelbottom = False, bottom = False)


all_axes = fig.get_axes()
for ax in all_axes:
    for sp in ax.spines.values():
        sp.set_visible(False)

fig.set_tight_layout(True)

plt.savefig('../output/SpatialDistance/img.png', dpi=500,  facecolor='white', transparent=False)
plt.close()














