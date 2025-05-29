import pandas as pd

strikesLocalCoordinates = pd.read_csv('../output/StrikesCoordinates/strikesLocalCoordinates.csv')

strikesMonitoringTime = pd.read_csv('../output/TablesTime/taballstrikes_timetolastimage.csv')

df_merged = pd.merge(strikesLocalCoordinates[['nstrike', 'Xlocal', 'Ylocal']], strikesMonitoringTime[['nstrike','datestrike', 'diflastimg']], on='nstrike')

# Arredondar as colunas para duas casas decimais
df_merged['Xlocal'] = df_merged['Xlocal'].round(1)
df_merged['Ylocal'] = df_merged['Ylocal'].round(1)
df_merged['diflastimg'] = df_merged['diflastimg'].round(1)

# Renomear as colunas
df_merged = df_merged.rename(columns={
    'nstrike': 'Strike',
    'datestrike': 'DateStrike',
    'diflastimg': 'Drone(months)'
})

df_merged.to_csv('../output/StrikesCoordinates/tableSI.csv')