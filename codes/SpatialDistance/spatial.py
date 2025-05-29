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


strikes = gpd.read_file("../data/shapefiles/strikes_50ha_UTM_17N.shp")
gaps = gpd.read_file("../data/shapefiles/Merge_gaps_all_strikes_area.shp")

#First buffer 10 meters
buffer1 = strikes.geometry.buffer(10)

#Function to create buffer rings
#Two buffers and difference
def rings (strikes, meters):

    brings = strikes.geometry.buffer(meters-10)
    brings2 = strikes.geometry.buffer(meters)
    brings2dif = brings2.difference(brings)

    return brings2dif


#Select total gap area of each strike
listastrike= gaps.nstrike.unique()

i=0
coletor=[]
while i < len(listastrike):

    sel = gaps.loc[gaps['nstrike']==listastrike[i]]
    selmax = sel.loc[sel['date']==sel.date.max()]
    coletor.append(selmax)
    i+=1

gapsmax = pd.concat(coletor)

gapsmax.to_file('../output/SpatialDistance/gapsmax.shp')


#Call function
intervals = np.arange(20,41,10)

colrings = []
i=0
while i < len(intervals):
    #Function parameters: table, intervals
    brings2dif = rings(strikes, intervals[i])
    #colect rings
    colrings.append(brings2dif)

    i+=1


allbuffer = buffer1.append(colrings)

allbuffer.to_file('../output/SpatialDistance/allbuffer.shp')

namestrike = strikes.nstrike.values


####Attribute an id from 10 to 40 m to rings
#repeat names strike 4 times
namestrike1 = np.tile(namestrike,4)

allbufferdf = gpd.GeoDataFrame(allbuffer)
allbufferdf = allbufferdf.rename(columns={0:'geometry'}).set_geometry('geometry')

allbufferdf['nstrike'] = namestrike1

allbufferdf['idrings'] = np.repeat(np.arange(10,41,10),len(namestrike))

allbufferdf.to_file('../output/SpatialDistance/allbufferdf.shp')

##Union rings and gaps to calculate percents of area for each ring
#The column “area_gap_r” is the gap area for each distance threshold 
#and the column “percent_ar” is the percentage (%) of the total gap area (F_AREA)

nameunion = gapsmax.nstrike.values

col=[]
i=0
while i < len(nameunion):
    selallbufferdf = allbufferdf.loc[allbufferdf.nstrike==nameunion[i],:]
    
    selgapsmax = gapsmax.loc[gapsmax.nstrike==nameunion[i],:]
    
    selstrikes = strikes.loc[strikes.nstrike==nameunion[i],:]

    uniongapsrings = gpd.overlay(selallbufferdf,selgapsmax, how='union')

    uniongapsrings['area_gap_r']= uniongapsrings.area

    uniongapsrings['percent_area']= uniongapsrings['area_gap_r']/uniongapsrings['F_AREA'] *100
    seluniongapsrings = uniongapsrings.dropna()

    col.append(seluniongapsrings)
    i+=1


df_gaps_union = col[0].append(col[1:])

#Shapefile containing the percentages for each buffer threshold
df_gaps_union.to_file('../output/SpatialDistance/df_gaps_union.shp')





