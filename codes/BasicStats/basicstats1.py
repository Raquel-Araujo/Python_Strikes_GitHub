import numpy as np
import pandas as pd
from scipy import stats

##Stats of total damaged area of all strikes

gaps = pd.read_csv('../data/csv/Merge_gaps_all_strikes_area.csv')


###Maximum canopy disturbance area for each strike
tabdin = pd.pivot_table(gaps, index='nstrike', values='F_AREA', aggfunc='max')


##Sum of areas of all strikes = 2947 m2
# print(tabdin.sum().round(1))

##Average area of all strikes = 210.5 m2
##Minimum area = 18.9 m2 (strike 9)
##Maximum area = 691.4 m2 (Strike 3)
# print(tabdin.describe().round(1))

#Confidence interval (96.8 to 324.2 m2)
ci = stats.t.interval(alpha=0.95, df=len(tabdin)-1, loc=np.mean(tabdin), scale=stats.sem(tabdin))
# print(ci)
# print(np.round(ci,1))

