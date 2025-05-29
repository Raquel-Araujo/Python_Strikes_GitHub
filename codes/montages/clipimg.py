# Import system modules
import arcpy
from arcpy import env
from arcpy.sa import *
import glob
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import matplotlib.image as mpimg 
import matplotlib.gridspec as gridspec
import script_fazer_varios_figuras as func
from datetime import datetime


# Check out the ArcGIS Spatial Analyst extension license
arcpy.CheckOutExtension("Spatial")

#Overwrite files
env.overwriteOutput = True

# Set environment settings
env.workspace = "Q:/UAVSHARE/Raquel_BCI/Lightning/Figures/"

path = "Q:/UAVSHARE/Raquel_BCI/Lightning/Figures/Orthomosaics/"

listimgall = glob.glob(path+'*tif')

date = map(lambda x: str(x).split("Orthomosaic_")[1].split('_')[0], listimgall)


strikes = pd.read_csv("Q:/UAVSHARE/Raquel_BCI/Lightning/Figures/Shapefile/strikes_50ha_UTM_17N.csv")

strikes['datestrike'] =  pd.to_datetime(strikes['Strike_dat'], format='%d-%b-%y')

datestrike = strikes['datestrike']

#Strike out of plot
strikes = strikes.drop(18).reset_index(drop=True)

#Strike name
nstrike = np.array(strikes.nstrike)


####################################################
#Select images for each strike

date1 = pd.Series(date)

dateimg = pd.to_datetime(date1, format='%Y%m%d')

deltatime = ((dateimg - datestrike[0])/np.timedelta64(1,'M')).round(1)

def nearest(items, pivot):
    return min([i for i in items if i <= pivot], key=lambda x: abs(x - pivot))


#i is the index of the strike
i=0

while i < len(datestrike):

    datenearest = nearest(dateimg, datestrike[i])

    indice = np.where(dateimg==datenearest)[0]

    listindice = np.arange(indice, indice+12)

    #For each strike do:
    sx = strikes.loc[i,'X']

    sy = strikes.loc[i,'Y']

    #Distance
    dist = 30

    #Clip Extent
    imgextent = sx-dist, sy-dist, sx+dist, sy+dist

    imgextent_str= str(imgextent[0])+ ' '+str(imgextent[1])+ ' '+ str(imgextent[2])+ ' ' + str(imgextent[3]) 


    #Creating out_raster paths
    #Basename takes only the file name
    pathraster1 = np.array(map(lambda x: os.path.basename(str(x)), listimgall))
    pathraster = pathraster1[listindice]

    # Set the compression environment to PackBits (compression for TIFF files).
    arcpy.env.compression = "PackBits"

    caminho = "Q:/UAVSHARE/Raquel_BCI/Lightning/Figures/imgclip1/"+'strike'+str(nstrike[i])+'/'

    #Create the folder for each strike
    os.mkdir(caminho)

    j=0

    while j < len(pathraster):

        # Load image (out_raster is a resultant raster object)
        out_raster = Raster("./Orthomosaics/"+pathraster[j])

        clip = arcpy.Clip_management(out_raster,imgextent_str, caminho+pathraster[j], "#", "#", "NONE")

        j+=1

    i+=1


  