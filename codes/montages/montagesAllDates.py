import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg 
import matplotlib.gridspec as gridspec
import script_fazer_varias_figuras as func
from datetime import datetime
import os
import glob
import geopandas as gpd


###Codigo modificado para calcular o meses entre a data de todas as imagens (ortomosaicos) e a data dos raios
#Produzindo a tabela tabela_difmonths_eachstrike.csv'
###Existem partes que precisam ser deletadas e que nao sao usadas para ter a tabela final. Preciso limpar o codigo.
###Tabela final usada para produzir o grafico "cumulative_area_time1_flatlines.png"


strikes = gpd.read_file('../data/shapefiles/strikes_50ha_UTM_17N.shp')
gaps = gpd.read_file('../data/shapefiles/all_associated_gaps_cor_copy.shp')

taballimages = pd.read_csv('../data/csv/gaps_area_days_5years.csv')

# Date strike
strikes['datestrike'] =  pd.to_datetime(strikes['Strike_dat'], format='%d-%b-%y')
datestrike = strikes['datestrike']

#Strike name
nstrike = np.array(strikes.nstrike)

### Organizing looping for all strikes
pathallstrikes = '../data/imgclip/'

# liststrikesfolders = os.walk(pathallstrikes)
liststrikesfolders = glob.glob(pathallstrikes+'*')

coletortabelameses = []

j=0
while j < len(liststrikesfolders):

    path = liststrikesfolders[j]+'/'

    listimg = glob.glob(path+'*tif')

    #List of image names
    #Basename takes only the file name
    pathraster = list(map(lambda x: os.path.basename(str(x)), listimg))


    #List of image dates
    date = list(map(lambda x: str(x).split("Orthomosaic_")[1].split('_')[0], pathraster))
    print(date)

    #Add hyphen to image dates
    dateimg = []
    i=0
    while i < len(date):
        datecor = datetime.strptime(date[i],'%Y%m%d').date().isoformat()
        dateimg.append(datecor)
        i+=1

    ##Filter strike
    # Strike name for this filter
    namestrikefilter = str(path).split("e")[1].split('/')[0]

    strikesel = strikes.loc[strikes.nstrike==namestrikefilter]

    #Filter gaps
    gapstrike = gaps.loc[gaps.nstrike==namestrikefilter]

    # Image extent
    sx = strikesel.loc[:,'X']
    sx= float(sx.to_string(index=False))

    sy = strikesel.loc[:,'Y']
    sy = float(sy.to_string(index=False))

    #Distance
    dist = 30

    #Image extent = [long left, long right, lat bottom, lat top]
    # imgextent1 = [626362.958459, 626422.958459, 1.011952e+06, 1.012012e+06]
    imgextent = sx-dist, sx+dist, sy-dist, sy+dist

    #Plot

    #Read images
    i=0
    objimg = []
    while i < len(listimg):
        img = mpimg.imread(listimg[i])
        objimg.append(img)

        i+=1


    ### define o tamnho da figura em polegadas [largura, altura]
    size=[8,6]
    ### define a quantidade de subdivisao da figura [numero de linhas, numero de colunas]
    grid=[3,4]

    #### define pasta e nome de arquivo
    outputdir = '../output/montages/'

    output= outputdir +'strike'+namestrikefilter+'.png'

    nomestrike = 'Strike ' +namestrikefilter+ ': '+str(strikesel.datestrike.values[0]).split('T')[0]

    #### Time in month (difference of image date to strike occurrence)
    dateimg1 = pd.to_datetime(dateimg, format='%Y-%m-%d')

    dateallimages = pd.to_datetime(taballimages.date, format='%Y-%m-%d')

    deltatime = []
    for sel in dateallimages:
        deltatime.append((((sel - strikesel.datestrike)/np.timedelta64(1,'M')).round(1)).values[0])

    df = pd.DataFrame({'nstrike': [namestrikefilter] * len(deltatime), 'difmonth': deltatime})

    coletortabelameses.append(df)

    j+=1

result = pd.concat(coletortabelameses, ignore_index=True, axis=0)

result.to_csv('../output/montages/tabela_difmonths_eachstrike.csv')