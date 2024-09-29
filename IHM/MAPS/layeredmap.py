import folium
import pandas as pd
import pyodbc
import requests

# Informations de connexion à la base de données
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

# Chargement des données
sql_datas = pd.read_sql_query(
    """
    SELECT
    T_PAYS_PYS.PYS_NOM, T_DATA_DTA.DTA_VALEUR, T_DATA_DTA.DTA_NOM
    FROM T_DATA_DTA
    LEFT OUTER JOIN T_PAYS_PYS ON T_PAYS_PYS.PYS_ID = T_DATA_DTA.PYS_ID
    LEFT OUTER JOIN T_DATE_DAT ON T_DATE_DAT.DAT_ID = T_DATA_DTA.DAT_ID
    WHERE T_DATE_DAT.DAT_DATE = '2021-01-01'
    """,
    conn,
)

# Nettoyage et filtrage de tout les dataframes utilisés, en ne gardant que les données utiles
df_SQLTEST = pd.DataFrame(sql_datas)
df_datas_co2 = df_SQLTEST[(df_SQLTEST['DTA_NOM'] == 'Annual CO2 emissions per capita')]
df_datas_pluvio = df_SQLTEST[(df_SQLTEST['DTA_NOM'] == 'Annual Precipitation')]
df_datas_temp = df_SQLTEST[(df_SQLTEST['DTA_NOM'] == 'Annual Temperature')]

df_datas_co2 = df_datas_co2.dropna(subset=['DTA_VALEUR'])
df_datas_co2.columns = ['Country', 'Valeur', 'Type']
df_datas_co2['Valeur'] = pd.to_numeric(df_datas_co2['Valeur'] , errors='coerce')

df_datas_pluvio = df_datas_pluvio.dropna(subset=['DTA_VALEUR'])
df_datas_pluvio.columns = ['Country', 'Valeur', 'Type']
df_datas_pluvio['Valeur'] = pd.to_numeric(df_datas_pluvio['Valeur'] , errors='coerce')

df_datas_temp = df_datas_temp.dropna(subset=['DTA_VALEUR'])
df_datas_temp.columns = ['Country', 'Valeur', 'Type']
df_datas_temp['Valeur'] = pd.to_numeric(df_datas_temp['Valeur'] , errors='coerce')

# Chargement du GeoJSON
countries_geojson_url = 'https://raw.githubusercontent.com/datasets/geo-countries/master/data/countries.geojson'
geojson_data = requests.get(countries_geojson_url).json()

# Style pour le fond de carte
style1 = {'fillColor': '#eaf9ba', 'color': '#c6df79', 'backgroundColor': '#634643'}

# Création de la carte de base
m = folium.Map(location=(30, 10), zoom_start=3, tiles='cartodb positron')

# Ajout du fond de carte GeoJSON
folium.GeoJson(
    geojson_data,
    style_function=lambda x: style1,
    name="countries"
).add_to(m)

# Fonction pour ajouter des données au GeoJSON
def add_choropleth(map_obj, data, layer_name, column_name, fill_color):
    choropleth = folium.Choropleth(
        geo_data=geojson_data,
        data=data,
        columns=["Country", column_name],
        key_on="feature.properties.ADMIN",
        fill_color=fill_color,
        fill_opacity=0.8,
        line_opacity=0.3,
        nan_fill_color="white",
        name=layer_name
    ).add_to(map_obj)
    
# Ajout des couches de données, une par une 
add_choropleth(m, df_datas_co2, 'CO2 Emissions', 'Valeur', 'OrRd')
add_choropleth(m, df_datas_temp, 'Températures', 'Valeur', 'RdYlBu_r')
add_choropleth(m, df_datas_pluvio, 'Pluviométrie', 'Valeur', 'BuPu')

# Ajout du contrôle des calques
folium.LayerControl().add_to(m)

# Sauvegarde de la carte dans un fichier HTML
m.save('map_with_layers_and_tooltips.html')
