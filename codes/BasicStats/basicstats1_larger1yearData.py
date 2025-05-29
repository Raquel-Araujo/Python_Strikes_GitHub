import numpy as np
import pandas as pd

##Stats of total damaged area of strikes  with at least 1 year of imagery data

gaps = pd.read_csv('../data/csv/Merge_gaps_all_strikes_area.csv')
# print(gaps)

# Remover as linhas com menos de 1 ano de dados(strikes 19001 e 19021)
# ~: Inverte o resultado, ou seja, seleciona as linhas onde a condição é False.
gaps = gaps[~gaps['nstrike'].isin(['19001', '19021'])]
# print(gaps)

###Maximum canopy disturbance area for each strike
tabdin = pd.pivot_table(gaps, index='nstrike', values='F_AREA', aggfunc='max')
# print(tabdin)

##Sum of areas of all strikes = 2838 m2
# print(tabdin.sum().round(1))

##Average area of all strikes = 236.5 m2
##Minimum area = 18.9 m2 (strike 9)
##Maximum area = 691.4 m2 (Strike 3)
# print(tabdin.describe().round(1))



