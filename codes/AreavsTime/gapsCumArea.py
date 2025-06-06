import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
from scipy import stats
import matplotlib.cm as cm
# import matplotx


tabstrikes = pd.read_csv('../data/csv/Merge_gaps_all_strikes_area.csv')
tabdatestrikes = pd.read_csv('../data/csv/strikes_50ha_UTM_17N.csv')

tabdifmonth = pd.read_csv('../output/montages/tabela_difmonths_eachstrike.csv')


######
#Remover a primeira coluna com os indices
tabdifmonth = tabdifmonth.iloc[:, 1:]
##Filtrar os valores que difmonths sao negativos
tabdifmonth = tabdifmonth[tabdifmonth['difmonth'] >= 0]


######
tabdatestrikes['datestrike'] = pd.to_datetime(tabdatestrikes.Strike_dat, format='%d-%b-%y')

# Merge the column datestrike, keeping one date of each strike
data = tabdatestrikes.loc[:,['nstrike','datestrike']].drop_duplicates()

tabstrikes = pd.merge(tabstrikes,data,on='nstrike', how='left')


#Differences of dates
tabstrikes['dategap'] = pd.to_datetime(tabstrikes.date, format='%Y/%m/%d')

tabstrikes['month'] = (tabstrikes.dategap - tabstrikes.datestrike)/np.timedelta64(1, 'M')

tabdin = pd.pivot_table(tabstrikes, index='nstrike', values='month', aggfunc=np.max)

ci = stats.t.interval(alpha=0.95, df=len(tabdin)-1, loc=np.mean(tabdin), scale=stats.sem(tabdin))


#Difference of last image
datelastimg = pd.to_datetime('2019-11-28', format='%Y-%m-%d')
tabstrikes['diflastimg'] = (datelastimg - tabstrikes.datestrike)/np.timedelta64(1, 'M')


##########################
#Create the names in the order of strike occurrence
datastrike = tabdatestrikes.loc[:,['nstrike', 'datestrike']].sort_values('datestrike')

###########
nome2 = datastrike.nstrike.values
nome1 = np.unique(tabstrikes.nstrike)

nome = nome2[np.isin(nome2, nome1)]

colorstrike = cm.jet(np.linspace(0.1, 0.9, len(nome)))

plt.rcParams["font.family"] = "Times New Roman"
plt.rcParams['font.size'] = '12'
plt.figure(figsize=(8,4))

i=0
while i < len(nome):

    tabstrikes1 = tabstrikes.loc[tabstrikes.nstrike==nome[i], ['nstrike','F_AREA', 'month', 'diflastimg']]
    tabstrikes1 = tabstrikes1.round(1)

    ###Merge tables
    tabdifmonth1 = tabdifmonth.loc[tabdifmonth.nstrike==nome[i]]
    tabstrikes1 = pd.merge(tabstrikes1, tabdifmonth1, left_on='month',right_on='difmonth', how='outer')
    tabstrikes1 = tabstrikes1.sort_values(by='difmonth').reset_index(drop=True)

    # Create an array of zeros
    first = np.zeros((6,), dtype=int)

    # Attribute the index value and sort indexes ascending
    tabstrikes1.loc[min(tabstrikes1.index)-1] = first
    tabstrikes2 = tabstrikes1.sort_index(axis = 0)

    # Use o método fillna() para preencher os NaN na coluna com os valores da primeira linha acima do NaN
    tabstrikes2['F_AREA'].fillna(method='ffill', inplace=True)
    tabstrikes2.reset_index(drop=True, inplace=True)
    tabstrikes2['diflastimg'].fillna(method='ffill', inplace=True)
    tabstrikes2.drop(columns=['nstrike_x','month'], inplace=True)
    tabstrikes2.rename(columns={'nstrike_y':'nstrike', 'difmonth':'month'}, inplace=True)
    tabstrikes2=tabstrikes2[['nstrike', 'F_AREA', 'month', 'diflastimg']]


    #Copy the last row
    last = tabstrikes2.iloc[-1:]
    # Create a new line
    tabstrikes3 = tabstrikes2.append(last)
    tabstrikes3.iloc[-1,2] = tabstrikes3.iloc[-1,3]

    ##Doing this again to create the points of new canopy disturbances and do not modify the code
    tabstrikesDots = tabstrikes.loc[tabstrikes.nstrike==nome[i], ['nstrike','F_AREA', 'month', 'diflastimg']]
    tabstrikesDots = tabstrikesDots.round(1)

    plt.scatter(tabstrikes2.month, tabstrikes2.F_AREA, color=colorstrike[i], marker="|", linewidths=0.5, s=5)
    plt.scatter(tabstrikesDots.month, tabstrikesDots.F_AREA, color=colorstrike[i], marker="|", linewidths=1.3, s=15)
    plt.plot(tabstrikes3.month, tabstrikes3.F_AREA, label=nome[i], color=colorstrike[i],linewidth=1)

    i+=1


plt.ylabel('Cumulative canopy area disturbed (m$^2$)')
plt.xlabel('Months post-strike')
xposition = [12, 24, 36]
for xc in xposition:
    plt.axvline(x=xc, color='gray', linestyle='--',linewidth=0.8)

plt.savefig('../output/AreavsTime/cumulative_area_time.png', dpi=300, bbox_inches='tight')
plt.close()

