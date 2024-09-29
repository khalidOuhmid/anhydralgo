import numpy as np
import pandas as pd
import plotly.express as px
import pyodbc
import geopandas as gpd

# Paramètres de connexion à la base de données
server = 'INFO-MSSQL-ETD'
database = 'SAE_TEAM55'
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

# Chargement des données requises 
sql_query = """
SELECT T_DATE_DAT.DAT_DATE, T_PAYS_PYS.PYS_NOM, T_DATA_DTA.DTA_VALEUR, T_ACTIVITY_ACT.ACT_NOM
FROM T_DATA_DTA
LEFT OUTER JOIN T_PAYS_PYS ON T_PAYS_PYS.PYS_ID = T_DATA_DTA.PYS_ID
LEFT OUTER JOIN T_DATE_DAT ON T_DATE_DAT.DAT_ID = T_DATA_DTA.DAT_ID
INNER JOIN T_ACTIVITY_ACT ON T_ACTIVITY_ACT.ACT_ID = T_DATA_DTA.ACT_ID
WHERE T_DATE_DAT.DAT_DATE >= '1990-01-01'
AND T_PAYS_PYS.PYS_NOM IN ('France', 'Germany', 'Ivory Coast', 'China', 'India', 'Denmark', 'United States')
AND T_DATA_DTA.DTA_NOM = 'Emission Data' AND T_DATA_DTA.DTA_UNITE = 'CO2'
"""

df_datas_co2 = pd.read_sql_query(sql_query, conn)
df_datas_co2['DTA_VALEUR'] = pd.to_numeric(df_datas_co2['DTA_VALEUR'], errors='coerce')
df_datas_co2 = df_datas_co2.dropna(subset=['DTA_VALEUR'])
df_datas_co2.columns = ['Year', 'Country', 'CO2', 'Activity']
df_datas_co2['Year'] = pd.to_datetime(df_datas_co2['Year']).dt.year.astype(str)

# Agrégation des données par pays et année pour obtenir les émissions totales pour chaque pays chaque année
df_country_total = df_datas_co2.groupby(['Country', 'Year']).agg({'CO2': 'sum'}).reset_index()

# Calcul des émissions totales pour chaque activité pour chaque pays chaque année
df_activity_total = df_datas_co2.groupby(['Country', 'Year', 'Activity']).agg({'CO2': 'sum'}).reset_index()

# Fusion des émissions totales pour chaque activité pour chaque pays chaque année avec le dataframe agrégé
df_activity_total = pd.merge(df_activity_total, df_country_total, on=['Country', 'Year'], suffixes=('', '_total'))

# Calcul du ourcentage des émissions pour chaque activité dans les émissions totales pour chaque pays chaque année
df_activity_total['Percentage_of_Total'] = (df_activity_total['CO2'] / df_activity_total['CO2_total']) * 100

# Charger les données GeoJSON
countries_geojson = 'https://raw.githubusercontent.com/datasets/geo-countries/master/data/countries.geojson'
geo_data = gpd.read_file(countries_geojson)

# Simplifier les géométries pour réduire la taille
def simplify_geometry(geometry, tolerance=0.01):
    return geometry.simplify(tolerance, preserve_topology=True)

geo_data['geometry'] = geo_data['geometry'].apply(simplify_geometry)

# Création de la carte choroplèthe avec Plotly
fig = px.choropleth_mapbox(
    data_frame=df_country_total,
    geojson=geo_data.__geo_interface__, 
    locations='Country',
    featureidkey="properties.ADMIN", 
    color='CO2',
    center={'lat': 20, 'lon': 0}, 
    mapbox_style='carto-positron',
    zoom=1.5, 
    color_continuous_scale='Greys', 
    range_color=(df_country_total['CO2'].min(), df_country_total['CO2'].max()),  
    animation_frame='Year',
    width=800,
    height=600,
    hover_name='Country',
    labels={'CO2': 'Total Emissions'}
)

# Ajout du pourcentage de chaque activité dans les émissions totales pour chaque pays chaque année au texte de survol
hover_text = []
for index, row in df_country_total.iterrows():
    country = row['Country']
    year = row['Year']
    total_emissions = row['CO2']
    activity_info = ""
    for _, activity_row in df_activity_total[(df_activity_total['Country'] == country) & (df_activity_total['Year'] == year)].iterrows():
        activity_info += f"{activity_row['Activity']}: {activity_row['Percentage_of_Total']:.2f}%<br>"
    hover_text.append(f"Country: {country}<br>Total Emissions: {total_emissions:.2f}<br>{activity_info}")

# Mise à jour le texte de survol pour chaque frame
fig.update_traces(hovertext=hover_text, hoverinfo="text")

# Enregistrer et afficher la carte
fig.write_html('30YoCO2.html')
fig.show()
