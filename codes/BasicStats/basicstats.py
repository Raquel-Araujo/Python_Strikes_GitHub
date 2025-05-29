import numpy as np
import pandas as pd
from scipy import stats

##Stats of mean, minimmum and maximum and confidence interval of disturbance polygons of each strike
#And percents of standing dead trees, branchfalls and treefalls


gaps = pd.read_csv('../data/csv/gapstrikes_join_heightdrop.csv')
print(gaps)

#50 gap polygons
# print(len(gaps.area_m2))
 
list = [gaps.treefall, gaps.grbranch, gaps.brbranch, gaps.standing]

countclass = []

for i in list:
    soma = i.sum() ##sum of numbers 1
    countclass.append(soma)

total = sum(countclass)

#Percents of total number = [ 6. 12. 14. 68.]
perc = (countclass/total)*100


list = [gaps.treefall, gaps.grbranch, gaps.brbranch, gaps.standing]

countAreaClass = []

for i in list:
    condition = i==1
    gapsAreaClass = gaps.loc[condition]

    somaAreaClass = gapsAreaClass.area_m2.sum()

    countAreaClass.append(somaAreaClass)


AreaTotal = gaps.area_m2.sum()

percentArea = ((countAreaClass/AreaTotal)*100).round(1)


###Mean, mininum and maximum canopy disturbance for each strike
tabdin = pd.pivot_table(gaps, index='nstrike', values='area_m2', aggfunc='mean')
print(tabdin)

#Average of 63.6 m2
#Min = 18.9 m2
#Max = 165.5 m2
# print(tabdin.describe().round(1))

#Confidence interval (38.4 to 88.8)
ci = stats.t.interval(alpha=0.95, df=len(tabdin)-1, loc=np.mean(tabdin), scale=stats.sem(tabdin))
# print(ci)
# print(np.round(ci,1))


