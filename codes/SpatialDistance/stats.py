import pandas as pd
import numpy as np

gapsrings = pd.read_csv('../output/SpatialDistance/df_gaps_union.csv')


sumarea_eachring = (gapsrings.groupby('idrings').area_gap_r.sum())

totalareastrike = gapsrings.F_AREA.unique().sum()

percent_eachring = (sumarea_eachring/totalareastrike)*100

percent_eachring = percent_eachring.round(2)

### Calcular o desvio padrão ponderado
#Primeiro fazer uma tabela preenchendo todos os valores de idrings para todos os raios

# Lista dos valores desejados para idrings
idrings_values = [10, 20, 30, 40]

# Criar um novo DataFrame com todas as combinações possíveis
def completar_idrings(df):
    new_rows = []
    
    for nstrike, group in df.groupby("nstrike_1"):
        existing_idrings = set(group["idrings"])
        F_AREA = group["F_AREA"].iloc[0]  # Mantém o mesmo valor de F_AREA
        
        for idrings in idrings_values:
            if idrings not in existing_idrings:
                new_rows.append({
                    "nstrike_1": nstrike,
                    "idrings": idrings,
                    "Id": 0,
                    "nstrike_2": 0,
                    "date": None,
                    "F_AREA": F_AREA,
                    "area_gap_r": 0,
                    "percent_ar": 0
                })
    
    df_completed = pd.concat([df, pd.DataFrame(new_rows)], ignore_index=True)
    df_completed.sort_values(by=["nstrike_1", "idrings"], inplace=True)
    return df_completed

#Exemplo de uso
df_novo = completar_idrings(gapsrings)

# Agora calcular o desvio padrão ponderado
def weighted_std(group):
    weights = group['F_AREA']
    values = group['percent_ar']
    mean_w = np.average(values, weights=weights)
    variance_w = np.average((values - mean_w) ** 2, weights=weights)
    return np.sqrt(variance_w)


std_eachring = df_novo.groupby('idrings').apply(weighted_std)
std_eachring = std_eachring.round(2)

percent_eachring.to_csv('../output/SpatialDistance/stats_weighted_mean_percent_rings.csv')
std_eachring.to_csv('../output/SpatialDistance/stats_weighted_std_percent_rings.csv')





