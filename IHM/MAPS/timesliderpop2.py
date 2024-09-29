import numpy as np
import pandas as pd
import plotly.graph_objects as go
import pyodbc
import geopandas as gpd

# Paramètres de connexion
server = 'INFO-MSSQL-ETD'
database = 'SAE_TEAM5'
username = 'etd05'
password = 'fqnsbtc4'

# Connexion à la base de données
try:
    conn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        f'SERVER={server};'
        f'DATABASE={database};'
        f'UID={username};'
        f'PWD={password}'
    )
    print("Connexion réussie à la base de données")
except pyodbc.Error as e:
    print("Erreur de connexion : ", e)
    exit()

# Chargement des données nécessaires. 
sql_query = """
SELECT T_DATE_DAT.DAT_DATE, T_PAYS_PYS.PYS_NOM, T_DATA_DTA.DTA_VALEUR
FROM T_DATA_DTA
LEFT OUTER JOIN T_PAYS_PYS ON T_PAYS_PYS.PYS_ID = T_DATA_DTA.PYS_ID
LEFT OUTER JOIN T_DATE_DAT ON T_DATE_DAT.DAT_ID = T_DATA_DTA.DAT_ID
WHERE T_DATE_DAT.DAT_DATE >= '1990-01-01'
AND T_PAYS_PYS.PYS_NOM IN ('France', 'Germany', 'Ivory Coast', 'China', 'India', 'Denmark', 'United States')
AND T_DATA_DTA.DTA_NOM = 'Population'
"""

df_datas_population = pd.read_sql_query(sql_query, conn)
df_datas_population['DTA_VALEUR'] = pd.to_numeric(df_datas_population['DTA_VALEUR'], errors='coerce')
df_datas_population = df_datas_population.dropna(subset=['DTA_VALEUR'])
df_datas_population.columns = ['Year', 'Country', 'Population']
df_datas_population['Year'] = pd.to_datetime(df_datas_population['Year']).dt.year.astype(str)

# Chargement des données geoJSON
countries_geojson = 'https://raw.githubusercontent.com/datasets/geo-countries/master/data/countries.geojson'
geo_data = gpd.read_file(countries_geojson)

# Simplification des polygones des pays
def simplify_geometry(geometry, tolerance=0.01):
    return geometry.simplify(tolerance, preserve_topology=True)

geo_data['geometry'] = geo_data['geometry'].apply(simplify_geometry)

# Définition de ranges personalisées pour les couleurs 
min_population = df_datas_population['Population'].min()
max_population = df_datas_population['Population'].max()

# Calcul des tranches 
tranche_1 = 0.05 * max_population
tranche_2 = 0.1 * max_population
tranche_3 = 0.2 * max_population
tranche_4 = 0.3 * max_population
tranche_5 = 0.45 * max_population
tranche_6 = 0.55 * max_population
tranche_7 = 0.7 * max_population
tranche_8 = 0.9 * max_population

# Check l'absence de ranges nulles
if any(pd.isna([tranche_1, tranche_2, tranche_3, tranche_4, tranche_5, tranche_6, tranche_7, tranche_8])):
    raise ValueError("One of the range steps is NaN. Please check the population data.")

# Definition du schéma de couleurs 
colorscale = [
    (0, 'rgb(255, 255, 255)'),
    (tranche_1 / max_population, 'rgb(255, 230, 230)'),
    (tranche_2 / max_population, 'rgb(255, 204, 204)'),
    (tranche_3 / max_population, 'rgb(255, 179, 179)'),
    (tranche_4 / max_population, 'rgb(255, 153, 153)'),
    (tranche_5 / max_population, 'rgb(255, 128, 128)'),
    (tranche_6 / max_population, 'rgb(255, 102, 102)'),
    (tranche_7 / max_population, 'rgb(255, 77, 77)'),
    (tranche_8 / max_population, 'rgb(255, 51, 51)'),
    (1, 'rgb(255, 0, 0)')
]

# Création de la carte initiale
fig = go.Figure()

# Création des cartes pour chaque année
years = df_datas_population['Year'].unique()
frames = []
for year in years:
    frame_data = df_datas_population[df_datas_population['Year'] == year]
    frame = go.Choroplethmapbox(
        geojson=geo_data.__geo_interface__,
        locations=frame_data['Country'],
        z=frame_data['Population'],
        featureidkey="properties.ADMIN",
        colorscale=colorscale,
        colorbar=dict(
            title='Population',
            tickvals=[0, tranche_1, tranche_2, tranche_3, tranche_4, tranche_5, tranche_6, tranche_7, tranche_8, max_population],
            ticktext=['0', f'{int(tranche_1)}', f'{int(tranche_2)}', f'{int(tranche_3)}', f'{int(tranche_4)}', f'{int(tranche_5)}', f'{int(tranche_6)}', f'{int(tranche_7)}', f'{int(tranche_8)}', f'{int(max_population)}']
        ),
        hoverinfo='location+z',
        name=year
    )
    frames.append(go.Frame(data=[frame], name=year))

# Ajout des données de la première carte 
initial_data = df_datas_population[df_datas_population['Year'] == years[0]]
fig.add_trace(go.Choroplethmapbox(
    geojson=geo_data.__geo_interface__,
    locations=initial_data['Country'],
    z=initial_data['Population'],
    featureidkey="properties.ADMIN",
    colorscale=colorscale,
    colorbar=dict(
        title='Population',
        tickvals=[0, tranche_1, tranche_2, tranche_3, tranche_4, tranche_5, tranche_6, tranche_7, tranche_8, max_population],
        ticktext=['0', f'{int(tranche_1)}', f'{int(tranche_2)}', f'{int(tranche_3)}', f'{int(tranche_4)}', f'{int(tranche_5)}', f'{int(tranche_6)}', f'{int(tranche_7)}', f'{int(tranche_8)}', f'{int(max_population)}']
    ),
    hoverinfo='location+z',
))

# Ajout du slider temporel et du colorframe sur la carte 
fig.update_layout(
    mapbox_style='carto-positron',
    mapbox_zoom=1.5,
    mapbox_center={'lat': 20, 'lon': 0},
    width=800,
    height=600,
    updatemenus=[{
        'buttons': [
            {
                'args': [None, {'frame': {'duration': 1000, 'redraw': True}, 'fromcurrent': True}],
                'label': 'Play',
                'method': 'animate'
            },
            {
                'args': [[None], {'frame': {'duration': 0, 'redraw': True}, 'mode': 'immediate', 'transition': {'duration': 0}}],
                'label': 'Pause',
                'method': 'animate'
            }
        ],
        'direction': 'left',
        'pad': {'r': 10, 't': 87},
        'showactive': False,
        'type': 'buttons',
        'x': 0.1,
        'xanchor': 'right',
        'y': 0,
        'yanchor': 'top'
    }],
    sliders=[{
        'active': 0,
        'yanchor': 'top',
        'xanchor': 'left',
        'currentvalue': {
            'font': {'size': 20},
            'prefix': 'Year:',
            'visible': True,
            'xanchor': 'right'
        },
        'transition': {'duration': 300, 'easing': 'cubic-in-out'},
        'pad': {'b': 10, 't': 50},
        'len': 0.9,
        'x': 0.1,
        'y': 0,
        'steps': [{
            'args': [[year], {'frame': {'duration': 300, 'redraw': True}, 'mode': 'immediate', 'transition': {'duration': 300}}],
            'label': year,
            'method': 'animate'
        } for year in years]
    }]
)

fig.frames = frames

# Sauvegarde de la carte
fig.write_html('30YPopulation.html')
fig.show()
