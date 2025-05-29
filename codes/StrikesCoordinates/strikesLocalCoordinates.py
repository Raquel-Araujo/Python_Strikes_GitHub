import geopandas as gpd
from shapely.geometry import LineString

BCIplot = gpd.read_file('../data/shapefiles/BCI_50ha_plot_WGS84_UTM17N.shp')
strikes = gpd.read_file('../data/shapefiles/strikes_50ha_UTM_17N.shp')


# Supondo que o polígono de interesse está na primeira linha do GeoDataFrame
poligono = BCIplot.geometry.iloc[0]

# Obtenha os vértices do polígono
# poligono.exterior.coords: Retorna os vértices do polígono.
coords = list(poligono.exterior.coords)

# Encontrar os dois vértices mais à esquerda (menor X) para a linha lateral esquerda
left_line_coords = sorted(coords, key=lambda x: x[0])[:2]  # Ordena pelo X e pega os dois primeiros

# Encontrar os dois vértices mais baixos (menor Y) para a linha inferior
bottom_line_coords = sorted(coords, key=lambda x: x[1])[:2]  # Ordena pelo Y e pega os dois primeiros

# Criar as linhas
left_line = LineString(left_line_coords)
bottom_line = LineString(bottom_line_coords)

# Criar um novo GeoDataFrame para as linhas
gdf_lines = gpd.GeoDataFrame(geometry=[left_line, bottom_line], crs=BCIplot.crs)

# Exibir o resultado
gdf_lines.to_file("../output/StrikesCoordinates/linhasParcela.shp")


# Calcular a distância ortogonal de cada ponto do geodataframe strikes para a linha lateral esquerda
strikes['Xlocal'] = strikes.geometry.apply(lambda point: point.distance(left_line))

# Calcular a distância ortogonal de cada ponto do geodataframe strikes para a linha inferior
strikes['Ylocal'] = strikes.geometry.apply(lambda point: point.distance(bottom_line))

# Exibir as primeiras linhas do GeoDataFrame strikes com as novas colunas
# print(strikes[['nstrike', 'Xlocal', 'Ylocal']])

#Exportar a tabela como csv
strikes[['nstrike', 'X', 'Y' ,'Xlocal', 'Ylocal']].to_csv('../output/StrikesCoordinates/strikesLocalCoordinates.csv')
