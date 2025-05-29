import numpy as np
import pandas as pd
from scipy import stats

##Stats of damaged volume of strikes with at least 1 year of imagery data

gaps = pd.read_csv('../output/TableVolume/tab_strikes_area_hdrop_volume.csv')

# Remover as linhas com menos de 1 ano de dados(strikes 19001 e 19021)
# ~: Inverte o resultado, ou seja, seleciona as linhas onde a condição é False.
gaps = gaps[~gaps['nstrike'].isin(['19001', '19021'])]

##Total volume of gaps = 30484.3 m3
# print(gaps.volume.sum().round(1))

##Basic stats of volume of all strikes
tabdin = pd.pivot_table(gaps, index='nstrike', values='volume', aggfunc=np.sum)

##Average volume of all strikes =  2540.4 m3
##Minimum volume = 66.4 m3 (strike 18012)
##Maximum volume = 10810.2 m3 (Strike 3)
# print(tabdin.describe().round(1))

#Confidence interval (340.1 to 4740.6 m3)
ci = stats.t.interval(alpha=0.95, df=len(tabdin)-1, loc=np.mean(tabdin), scale=stats.sem(tabdin))
# print(ci)
# print(np.round(ci,1))