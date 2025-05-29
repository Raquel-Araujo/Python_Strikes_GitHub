import pandas as pd
import numpy as np

gaps = pd.read_csv('../data/csv/Merge_gaps_all_strikes_area.csv')

strikes = np.unique(gaps.nstrike)

tabstrikes = pd.read_csv('../output/TablesTime/taballstrikes_timetolastimage.csv')

#Proportion strikes with gaps = 63.6%
proportion = (len(strikes)/len(tabstrikes.nstrike))*100

##############
#Remover strikes com menos de 1 ano de dados
# tabstrikes.loc[condição, 'nstrike']: Seleciona as linhas que satisfazem a condição e retorna apenas a coluna nstrike
strikeslarger12months = tabstrikes.loc[tabstrikes['diflastimg']>=12, 'nstrike']

# Encontrar os elementos que estão em ambos os conjuntos
intersecao = np.intersect1d(strikes, strikeslarger12months)

#Proportion strikes > 1 year of data with gaps = 66.7
proportionlarger12months = (len(intersecao)/len(strikeslarger12months))*100


################
#Selecionar na tabela dos raios, os raios que nao tiveram gaps
naointersecao = tabstrikes.loc[~tabstrikes['nstrike'].isin(strikes), :]

#Minimo do tempo de monitoramento dos raios que nao tiveram gaps = 4.5 meses
#Maximo do tempo de monitoramento dos raios que nao tiveram gaps  = 49.7 meses
# print(np.min(naointersecao.diflastimg).round(1))
# print(np.max(naointersecao.diflastimg).round(1))


############
##Tabela material suplementar
##Calcular o numero de raios e a proporcao de raios com pelo menos 12, 24, 36 meses de monitoramento
#E todos os raios (pelo menos 1 mes de monitoramento)

# tabstrikes.loc[condição, 'nstrike']: Seleciona as linhas que satisfazem a condição e retorna apenas a coluna nstrike

meses = [1,12,24,36]

coletornumero = []
coletorproporcao = []

for X in meses:

    strikeslargerXmonths = tabstrikes.loc[tabstrikes['diflastimg']>=X, 'nstrike']

    # Encontrar os elementos que estão em ambos os conjuntos
    intersecao = np.intersect1d(strikes, strikeslargerXmonths)


    #Proportion strikes > 1 year of data with gaps = 66.7
    proportionlargerXmonths = (len(intersecao)/len(strikeslargerXmonths))*100

    numeroStrikes = len(intersecao)
    proporcao = proportionlargerXmonths

    coletornumero.append(numeroStrikes)
    coletorproporcao.append(proporcao)


colunas = ['All', '12 months', '24 months' ,'36 months']


# Criando o DataFrame
df = pd.DataFrame({
    'Strikes with distubances': coletornumero,
    'Proportion strikes disturbances': coletorproporcao
}, index=colunas).T

df.round(1).to_csv('../output/BasicStats/tabSI_proportion_strikes.csv')






