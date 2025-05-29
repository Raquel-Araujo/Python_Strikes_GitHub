import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
from scipy import stats
import matplotlib.cm as cm
import statistics


tabstrikes = pd.read_csv('../data/csv/Merge_gaps_all_strikes_area.csv')
tabdatestrikes = pd.read_csv('../data/csv/strikes_50ha_UTM_17N.csv')


tabdatestrikes['datestrike'] = pd.to_datetime(tabdatestrikes.Strike_dat, format='%d-%b-%y')

# Merge the column datestrike, keeping one date of each strike
data = tabdatestrikes.loc[:,['nstrike','datestrike']].drop_duplicates()

##Merge tables of gaps and dates of strikes
tabstrikes = pd.merge(tabstrikes,data,on='nstrike', how='left')


#Differences of dates
tabstrikes['dategap'] = pd.to_datetime(tabstrikes.date, format='%Y/%m/%d')

tabstrikes['month'] = (tabstrikes.dategap - tabstrikes.datestrike)/np.timedelta64(1, 'M')


##How many months to reach the maximum area
tabdin = pd.pivot_table(tabstrikes, index='nstrike', values='month', aggfunc=np.max)

# Average time to reach maximum area = 12.9 months
# Minimum time = 0.8 months
# Maximum time = 23.9 months
# print(tabdin.describe().round(1))

months = np.array(tabdin)

##Standard deviation = 7.3 months
# print(np.std(months).round(1))

###Same analysis excluding 2 strikes (with gaps) inspected less than one year
tabdinless2strikes = tabdin.drop(['19001', '19021'])

# Average time to reach maximum area = 14.6 months
# Minimum time = 0.8 months
# Maximum time = 23.9 months
# print(tabdinless2strikes.describe().round(1))

months1 = np.array(tabdinless2strikes)

##Standard deviation = 6.5 months
# print(np.std(months1).round(1))


#Difference of last image
datelastimg = pd.to_datetime('2019-11-28', format='%Y-%m-%d')

tabstrikes['diflastimg'] = (datelastimg - tabstrikes.datestrike)/np.timedelta64(1, 'M')

tabstrikes.to_csv('../output/TablesTime/tabgapstrikes_timetolastimage.csv')

tabdatestrikes['diflastimg'] = (datelastimg - tabdatestrikes.datestrike)/np.timedelta64(1, 'M')
tabdatestrikes = tabdatestrikes.loc[:,['nstrike', 'datestrike', 'diflastimg']].reset_index(drop=True)

tabdatestrikes.to_csv('../output/TablesTime/taballstrikes_timetolastimage.csv')
