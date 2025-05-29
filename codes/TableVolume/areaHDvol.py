import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt

##This code calculates the volume for each date of gap occurrence
##The output is the table tab_strikes_area_hdrop_volume.csv
#The weighted average of height drop is calculated by sum(HD*area)/total area
# HD*area of each gap polygon
# total area is the sum of areas of gap polygons created on each date
##The volume is calculated by multiplying the total area by the weighted average of height drop

gapsmerge = pd.read_csv('../data/csv/Merge_gaps_all_strikes_area.csv')
tabheightdrop = pd.read_csv('../data/csv/gapstrikes_join_heightdrop.csv')

#Selecting columns
tabheightdropSel = tabheightdrop.loc[:,['date', 'area_m2', 'nstrike', 'Id', 'MEAN']]

#Correction of positive values
tabheightdropSel.loc[tabheightdropSel.MEAN>=0,'MEAN'] = -0.06

#list of nstrike
listaNStrike = list(set(tabheightdropSel.nstrike))

coletorTabela = pd.DataFrame(columns =['Id', 'nstrike', 'meanHD'])

k=0
while k < len(listaNStrike):

    #Select gaps of each strike
    strikeSel = tabheightdropSel.loc[tabheightdropSel.nstrike==listaNStrike[k]]

    #list of Ids
    listaId = sorted(list(set(strikeSel.Id)))

    #list nstrike to create the table
    listaStrike = list(set(strikeSel.nstrike))*len(listaId)

    coletormeanHD = []
    coletorarea = []
    j=0
    while j < len(listaId):

        #Select gaps of each Id (date)
        IdSel = strikeSel.loc[strikeSel.Id==listaId[j]]

        #list of indexes
        listaIndex = list(IdSel.index.values) 

        ##Sum of area of each date
        somaArea = np.sum(IdSel.area_m2)

        i=0
        coletor = []
        while i < len(listaIndex):
            #Area * mean height drop
            HDpond = IdSel.iloc[i,1]*IdSel.iloc[i,4]
            coletor.append(HDpond)

            i+=1

        somaHDpond = np.sum(coletor)
        
        meanHD = somaHDpond/somaArea
        coletormeanHD.append(meanHD)
        
        coletorarea.append(somaArea)

        j+=1


    
    tabHD = pd.DataFrame(list(zip(listaId, listaStrike, coletorarea, coletormeanHD)),columns =['Id', 'nstrike', 'area','meanHD'])
    
    coletorTabela = coletorTabela.append(tabHD, ignore_index = True)

    k+=1

gapsmerge = gapsmerge.iloc[:,0:3]


tabmergeHD = gapsmerge.merge(coletorTabela, left_on=['Id', 'nstrike'], right_on=['Id', 'nstrike'])
tabmergeHD['meanHDp'] = tabmergeHD['meanHD']*-1
tabmergeHD['volume'] = tabmergeHD.area*tabmergeHD.meanHDp


tabmergeHD.to_csv('../output/TableVolume/tab_strikes_area_hdrop_volume.csv')

