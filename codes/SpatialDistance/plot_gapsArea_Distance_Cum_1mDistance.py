import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
from scipy import stats
import matplotlib.cm as cm
# import matplotx


tabstrikes = pd.read_csv('../output/SpatialDistance/Figure1mDistance/df_gaps_union.csv')
weightedMean = pd.read_csv('../output/SpatialDistance/Figure1mDistance/stats_weighted_mean_percent_rings.csv')

###########

nome2 = tabstrikes.nstrike_1.values
nome1 = np.unique(tabstrikes.nstrike_1)

nome = nome2[np.isin(nome2, nome1)]

colorstrike = cm.jet(np.linspace(0.1, 0.9, len(nome)))

plt.rcParams["font.family"] = "Times New Roman"
plt.rcParams['font.size'] = '12'
plt.figure(figsize=(8,4))

col=[]
i=0
while i < len(nome):

    tabstrikes1 = tabstrikes.loc[tabstrikes.nstrike_1==nome[i], ['nstrike_1','percent_area', 'idrings']]
    print(tabstrikes1)
    print(nome[i])

    #####
    # coletando valores
    col.append(tabstrikes1.loc[:,['idrings', 'percent_area'] ])

    i+=1


# juntando tabelas e completando valores nulos com zero
# essa tabela tem a primeira coluna sendo as distancias (idrings)
# e as outras colunas sao as porcentagens dos danos para cada raio
from functools import reduce
ddf = reduce(lambda df1,df2: pd.merge(df1,df2,on='idrings', how='outer'), col).fillna(0)
ddf = ddf.sort_values(by='idrings', ascending=True)


### plot das linhas individuais
for i in range(len(ddf.columns)-1):
    plt.plot(ddf.idrings, ddf.iloc[:,i+1].cumsum(), label=nome[i], color=colorstrike[i],linewidth=1)

### media
weightedMean['cum'] = weightedMean['area_gap_r'].cumsum()

plt.plot(weightedMean.idrings.values, weightedMean.cum, color='k',linewidth=2) #linestyle='dashed'

plt.ylabel('Cumulative percentage of total canopy area disturbed (%)')
plt.xlabel('Distance (m)')
plt.xticks([0,10,20,30,40])
plt.savefig('../output/SpatialDistance/Figure1mDistance/plot_area_Distance_cumulative_all.png', dpi=300, bbox_inches='tight')
plt.close()