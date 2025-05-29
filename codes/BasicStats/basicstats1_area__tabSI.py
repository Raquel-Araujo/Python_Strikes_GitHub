import numpy as np
import pandas as pd

gaps = pd.read_csv('../data/csv/Merge_gaps_all_strikes_area.csv')

tabstrikes = pd.read_csv('../output/TablesTime/taballstrikes_timetolastimage.csv')

tabmerge = gaps.merge(tabstrikes[['nstrike', 'diflastimg']], on='nstrike')

######################
##Tabela SI

meses = [1,12,24,36]
coletor = []

for X in meses:

    tabstrikesTimeXmonths = tabmerge.loc[tabmerge.diflastimg>=X]

    tabdin = pd.pivot_table(tabstrikesTimeXmonths, index='nstrike', values='F_AREA', aggfunc='max')
    
    # Usando o método loc para selecionar as linhas
    estatisticas_selecionadas = tabdin.describe().loc[['mean', 'min', 'max']]

    coletor.append(estatisticas_selecionadas['F_AREA'].values)


colunas = ['All', '12 months', '24 months' ,'36 months']
linhas = [' Mean canopy disturbance area', 
        'Min canopy disturbance area', 'Max canopy disturbance area']

# Criar o DataFrame com os valores coletados
df_final = pd.DataFrame(data=coletor, columns=linhas).T

# Atribui as colunas
df_final.columns = colunas

df_final.round(1).to_csv('../output/BasicStats/tabSI_statsArea.csv')



