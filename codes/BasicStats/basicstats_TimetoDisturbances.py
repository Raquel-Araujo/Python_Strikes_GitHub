import numpy as np
import pandas as pd

tabstrikes = pd.read_csv('../output/TablesTime/tabgapstrikes_timetolastimage.csv')

###Minimum time to canopy disturbance to appear for each strike
tabdin = pd.pivot_table(tabstrikes, index='nstrike', values='month', aggfunc='min')

##Stats
#Count = 14
#Mean = 7.3
#Std = 4.7
#Min = 0.4
#Max = 14
# print(tabdin.describe().round(1))

###Minimum time to canopy disturbance to appear for each strike,
#taking to account strikes monitored to at least 24 months
#Select lines with diflastimg >= 24 months
tabstrikesTime24months = tabstrikes.loc[tabstrikes.diflastimg>=24]

tabdinmin = pd.pivot_table(tabstrikesTime24months, index='nstrike', values='month', aggfunc='min')


##Stats
#Count = 10
#Mean = 8.7
#Std = 4.4
#Min = 0.8
#Max = 14
# print(tabdinmin.describe().round(1))


###Maximum time to canopy disturbance to appear for each strike,
#taking to account strikes monitored to at least 24 months

#Select lines with diflastimg >= 24 months
tabstrikesTime24months = tabstrikes.loc[tabstrikes.diflastimg>=24]

tabdinmax = pd.pivot_table(tabstrikesTime24months, index='nstrike', values='month', aggfunc='max')


##Stats
#Count = 10
#Mean = 14.4
#Std = 7.5
#Min = 0.8
#Max = 23.9
# print(tabdinmax.describe().round(1))


############################
##Tabela material suplementar
###Minimum time to canopy disturbance to appear for each strike,
#taking to account strikes monitored to at least 1, 12, 24 and 36 months

meses = [1,12,24,36]
funcao = ['min', 'max']
nome = ['first', 'last']

i = 0
coldataframe = []

while i < len(funcao):

    # Reinicia o coletor para cada função
    coletor = []

    for X in meses:

        tabstrikesTimeXmonths = tabstrikes.loc[tabstrikes.diflastimg>=X]

        tabdinmin = pd.pivot_table(tabstrikesTimeXmonths, index='nstrike', values='month', aggfunc=funcao[i])
        
        # Usando o método loc para selecionar as linhas
        estatisticas_selecionadas = tabdinmin.describe().loc[['mean', 'std', 'min', 'max']]

        coletor.append(estatisticas_selecionadas['month'].values)


    colunas = ['All', '12 months', '24 months' ,'36 months']
    linhas = [' Mean time to ' +nome[i]+ ' disturbance', 'Std time to ' +nome[i]+ ' disturbance', 
            'Min time to ' +nome[i]+ ' disturbance', 'Max time to ' +nome[i]+ ' disturbance']

    # Criar o DataFrame com os valores coletados
    df_final = pd.DataFrame(data=coletor, columns=linhas).T

    # Atribui as colunas
    df_final.columns = colunas

    coldataframe.append(df_final)

    i+=1

# Concatena os DataFrames para `first` e `last` disturbance, resultando em 8 linhas
resultado_final = pd.concat(coldataframe)

resultado_final.round(1).to_csv('../output/BasicStats/tabSI_TimetoFirstLastDisturbances.csv')

