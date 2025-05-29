import numpy as np
import pandas as pd

tabproportion = pd.read_csv('../output/BasicStats/tabSI_proportion_strikes.csv')
tabarea = pd.read_csv('../output/BasicStats/tabSI_statsArea.csv')
tabvolume = pd.read_csv('../output/BasicStats/tabSI_statsVolume.csv')
tabtime = pd.read_csv('../output/BasicStats/tabSI_TimetoFirstLastDisturbances.csv')

result = pd.concat([tabproportion, tabarea, tabvolume, tabtime])
print(result)

result.to_csv('../output/BasicStats/tabSIallstats.csv')
