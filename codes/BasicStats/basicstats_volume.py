import numpy as np
import pandas as pd
from scipy import stats

##Stats of damaged volume of all strikes

gaps = pd.read_csv('../output/TableVolume/tab_strikes_area_hdrop_volume.csv')

##Total volume of gaps = 31335.3 m3
# print(gaps.volume.sum().round(1))

##Basic stats of volume of all strikes
tabdin = pd.pivot_table(gaps, index='nstrike', values='volume', aggfunc=np.sum)

##Average volume of all strikes = 2238.2 m3
##Minimum volume = 66.4 m3 (strike 18012)
##Maximum volume = 10810.2 m3 (Strike 3)
# print(tabdin.describe().round(1))

#Confidence interval (345 to 4131.4 m3)
ci = stats.t.interval(alpha=0.95, df=len(tabdin)-1, loc=np.mean(tabdin), scale=stats.sem(tabdin))
# print(ci)
# print(np.round(ci,1))

