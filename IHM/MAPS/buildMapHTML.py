import folium
import pandas as pd
import sqlite3
import pyodbc
import pycountry
import re
import pycountry_convert as pc
from folium.plugins import TimeSliderChoropleth

#Informations de la database
server = 'INFO-MSSQL-ETD'
database = 'SAE_TEAM5'
username = 'etd05'
password = 'fqnsbtc4'

#Connexion à la database
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

style1 = {'fillColor': '#eaf9ba', 'color': '#c6df79', 'backgroundColor':'#634643'}
countries_alt= ( 'https://raw.githubusercontent.com/datasets/geo-countries/master/data/countries.geojson')
timelayers = []

sql_datas = pd.read_sql_query(
    """
    SELECT
    *
    FROM T_DATA_DTA
    LEFT OUTER JOIN T_PAYS_PYS ON T_PAYS_PYS.PYS_ID = T_DATA_DTA.PYS_ID
    LEFT OUTER JOIN T_DATE_DAT ON T_DATE_DAT.DAT_ID = T_DATA_DTA.DAT_ID
    """,
    conn,
)

#Chargement des données dans différents dataframes
df_SQLTEST = pd.DataFrame(sql_datas)
df_datas_fossilsC02 = df_SQLTEST[(df_SQLTEST['DTA_NOM'] == 'Emission Data') & (df_SQLTEST['DTA_UNITE'] == 'CO2')]
df_datas_fossilsCH4 = df_SQLTEST[(df_SQLTEST['DTA_NOM'] == 'Emission Data') & (df_SQLTEST['DTA_UNITE'] == 'CH4')]
df_datas_fossilsN2O = df_SQLTEST[(df_SQLTEST['DTA_NOM'] == 'Emission Data') & (df_SQLTEST['DTA_UNITE'] == 'N2O')]
df_datas_pluvio = df_SQLTEST[(df_SQLTEST['DTA_NOM'] == 'Annual Precipitation')]
df_datas_pib = df_SQLTEST[(df_SQLTEST['DTA_NOM'] == 'GPD')]
df_datas_temp = df_SQLTEST[(df_SQLTEST['DTA_NOM'] == 'Annual Temperature')]

#Nettoyage et création des bins pour chaque df
df_datas_fossilsC02 = df_datas_fossilsC02.drop_duplicates(subset=["PYS_NOM"])
df_datas_fossilsC02['DTA_VALEUR'] = pd.to_numeric(df_datas_fossilsC02['DTA_VALEUR'], errors='coerce')
df_datas_fossilsC02 = df_datas_fossilsC02.dropna(subset=['DTA_VALEUR'])
bins_fossils = df_datas_fossilsC02['DTA_VALEUR'].quantile([0, 0.125, 0.25, 0.375, 0.5, 0.625, 0.75, 0.875, 1]).tolist()

df_datas_fossilsCH4 = df_datas_fossilsCH4.drop_duplicates(subset=["PYS_NOM"])
df_datas_fossilsCH4['DTA_VALEUR'] = pd.to_numeric(df_datas_fossilsCH4['DTA_VALEUR'], errors='coerce')
df_datas_fossilsCH4 = df_datas_fossilsCH4.dropna(subset=['DTA_VALEUR'])
bins_fossilsCH4 = df_datas_fossilsCH4['DTA_VALEUR'].quantile([0, 0.2, 0.3, 0.4, 0.5, 0.6, 0.9, 0.95, 1]).tolist()

df_datas_fossilsN2O = df_datas_fossilsN2O.drop_duplicates(subset=["PYS_NOM"])
df_datas_fossilsN2O['DTA_VALEUR'] = pd.to_numeric(df_datas_fossilsN2O['DTA_VALEUR'], errors='coerce')
df_datas_fossilsN2O = df_datas_fossilsN2O.dropna(subset=['DTA_VALEUR'])
bins_fossilsn2o = df_datas_fossilsN2O['DTA_VALEUR'].quantile([0, 0.125, 0.25, 0.375, 0.5, 0.625, 0.75, 0.875, 1]).tolist()

df_datas_pluvio = df_datas_pluvio.drop_duplicates(subset=["PYS_NOM"])
df_datas_pluvio['DTA_VALEUR'] = pd.to_numeric(df_datas_pluvio['DTA_VALEUR'], errors='coerce')
df_datas_pluvio = df_datas_pluvio.dropna(subset=['DTA_VALEUR'])
bins_pluvio = df_datas_pluvio['DTA_VALEUR'].quantile([0, 0.125, 0.25, 0.375, 0.5, 0.625, 0.75, 0.875, 1]).tolist()

df_datas_pib = df_datas_pib.drop_duplicates(subset=["PYS_NOM"])
df_datas_pib['DTA_VALEUR'] = pd.to_numeric(df_datas_pib['DTA_VALEUR'], errors='coerce')
df_datas_pib = df_datas_pib.dropna(subset=['DTA_VALEUR'])
bins_PIB = df_datas_pib['DTA_VALEUR'].quantile([0, 0.125, 0.25, 0.375, 0.5, 0.625, 0.75, 0.875, 1]).tolist()

df_datas_temp = df_datas_temp.drop_duplicates(subset=["PYS_NOM"])
df_datas_temp['DTA_VALEUR'] = pd.to_numeric(df_datas_temp['DTA_VALEUR'], errors='coerce')
df_datas_temp = df_datas_temp.dropna(subset=['DTA_VALEUR'])
bins_tmp = df_datas_temp['DTA_VALEUR'].quantile([0, 0.125, 0.25, 0.375, 0.5, 0.625, 0.75, 0.875, 1]).tolist()

#Création des options de la carte
map_options = {
    'location': (30, 10),
    'zoom_start': 3,
    'tiles': 'cartodb positron',
    'no_wrap': True
}

#Pour chaque carte, création de la map choropleth correspondante avec folium et save en HTML
m_fossils = folium.Map(location=(30, 10),zoom_start=3,tiles='cartodb positron')
folium.GeoJson(countries_alt, style_function=lambda x:style1, max_zoom=6, min_zoom=1).add_to(m_fossils)
folium.Choropleth(
    geo_data=countries_alt,
    data=df_datas_fossilsC02,
    columns=["PYS_NOM", "DTA_VALEUR"],
    key_on="feature.properties.ADMIN",
    fill_color='RdYlGn_r',
    fill_opacity=0.8,
    line_opacity=0.3,
    bins=bins_fossils,
    nan_fill_color="white",
    name="CO2 Emissions from Fossil Fuels per country"
).add_to(m_fossils)

m_fossils.save("mapFossilsCO2.html")

m_fossilsCH4 = folium.Map(location=(30, 10),zoom_start=3,tiles='cartodb positron')
folium.GeoJson(countries_alt, style_function=lambda x:style1, max_zoom=6, min_zoom=1).add_to(m_fossilsCH4)
folium.Choropleth(
    geo_data=countries_alt,
    data=df_datas_fossilsCH4,
    columns=["PYS_NOM", "DTA_VALEUR"],
    key_on="feature.properties.ADMIN",
    fill_color='Spectral_r',
    fill_opacity=0.8,
    line_opacity=0.3,
    bins=bins_fossilsCH4,
    nan_fill_color="white",
    name="CH4 Emissions from Fossil Fuels per country"
).add_to(m_fossilsCH4)

m_fossilsCH4.save("mapFossilsCH4.html")

m_fossilsn2o = folium.Map(location=(30, 10),zoom_start=3,tiles='cartodb positron')
folium.GeoJson(countries_alt, style_function=lambda x:style1, max_zoom=6, min_zoom=1).add_to(m_fossilsn2o)
folium.Choropleth(
    geo_data=countries_alt,
    data=df_datas_fossilsN2O,
    columns=["PYS_NOM", "DTA_VALEUR"],
    key_on="feature.properties.ADMIN",
    fill_color='Spectral_r',
    fill_opacity=0.8,
    line_opacity=0.3,
    bins=bins_fossilsn2o,
    nan_fill_color="white",
    name="N2O Emissions from Fossil Fuels per country"
).add_to(m_fossilsn2o)

m_fossilsn2o.save("mapFossilsN2O.html")

m_pluvio = folium.Map(location=(30, 10),zoom_start=3,tiles='cartodb positron')
folium.GeoJson(countries_alt, style_function=lambda x:style1, max_zoom=6, min_zoom=1).add_to(m_pluvio)
folium.Choropleth(
    geo_data=countries_alt,
    data=df_datas_pluvio,
    columns=["PYS_NOM", "DTA_VALEUR"],
    key_on="feature.properties.ADMIN",
    fill_color='Blues',
    fill_opacity=0.8,
    line_opacity=0.3,
    bins=bins_pluvio,
    nan_fill_color="white",
    name="Pluviometry by country"
).add_to(m_pluvio)

m_pluvio.save("mapPluvio.html")

m_pib = folium.Map(location=(30, 10),zoom_start=3,tiles='cartodb positron')
folium.GeoJson(countries_alt, style_function=lambda x:style1, max_zoom=6, min_zoom=1).add_to(m_pib)
folium.Choropleth(
    geo_data=countries_alt,
    data=df_datas_pib,
    columns=["PYS_NOM", "DTA_VALEUR"],
    key_on="feature.properties.ADMIN",
    fill_color='Reds',
    fill_opacity=0.8,
    line_opacity=0.3,
    bins=bins_PIB,
    nan_fill_color="white",
    name="GPD by country"
).add_to(m_pib)

m_pib.save("mapPIB.html")

m_temp = folium.Map(location=(30, 10),zoom_start=3,tiles='cartodb positron')
folium.GeoJson(countries_alt, style_function=lambda x:style1, max_zoom=6, min_zoom=1).add_to(m_temp)
folium.Choropleth(
    geo_data=countries_alt,
    data=df_datas_temp,
    columns=["PYS_NOM", "DTA_VALEUR"],
    key_on="feature.properties.ADMIN",
    fill_color='Spectral_r',
    fill_opacity=0.8,
    line_opacity=0.3,
    bins=bins_tmp,
    nan_fill_color="white",
    name="Temperature by country"
).add_to(m_temp)

m_temp.save("mapTemp.html")