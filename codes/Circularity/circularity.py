import pandas as pd
import numpy as np
import geopandas as gpd
import math
from scipy import stats


gapsmax = gpd.read_file('../output/SpatialDistance/gapsmax.shp')
## this is the total gap area of each strike

#Calculate perimeter
gapsmaxdf = gpd.GeoDataFrame(gapsmax)
gapsmaxdf['Perimeter'] = gapsmaxdf['geometry'].length

gapsmaxdf['Circularity'] = (4*math.pi*gapsmaxdf.F_AREA)/((gapsmaxdf.Perimeter)**2)

gapsmaxdf1 = gapsmaxdf.drop('geometry', axis=1)

gapsmaxdf1.to_csv('../output/Circularity/table_circularity.csv')

basicstats = gapsmaxdf.Circularity.describe().round(2)

ci = stats.t.interval(alpha=0.95, df=len(gapsmaxdf.Circularity)-1, loc=np.mean(gapsmaxdf.Circularity), scale=stats.sem(gapsmaxdf.Circularity))

basicstats.to_csv('../output/Circularity/basicstats_circularity.csv')

pd.DataFrame(ci).round(2).to_csv('../output/Circularity/ci_circularity.csv')



