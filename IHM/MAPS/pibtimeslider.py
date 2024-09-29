import numpy as np
import pandas as pd
import plotly.graph_objects as go
import pyodbc
import geopandas as gpd

# Paramètres de connexion à la base de données
serveur = 'INFO-MSSQL-ETD'
base_de_donnees = 'SAE_TEAM5'
utilisateur = 'etd05'
mot_de_passe = 'fqnsbtc4'

# Connexion à la base de données
try:
    conn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        f'SERVER={serveur};'
        f'DATABASE={base_de_donnees};'
        f'UID={utilisateur};'
        f'PWD={mot_de_passe}'
    )
    print("Connexion réussie à la base de données")
except pyodbc.Error as e:
    print("Erreur de connexion : ", e)
    exit()

# Chargement des données nécessaires depuis la base de données et filtrage pour des pays spécifiques
requete_sql = """
SELECT T_DATE_DAT.DAT_DATE, T_PAYS_PYS.PYS_NOM, T_DATA_DTA.DTA_VALEUR
FROM T_DATA_DTA
LEFT OUTER JOIN T_PAYS_PYS ON T_PAYS_PYS.PYS_ID = T_DATA_DTA.PYS_ID
LEFT OUTER JOIN T_DATE_DAT ON T_DATE_DAT.DAT_ID = T_DATA_DTA.DAT_ID
WHERE T_DATE_DAT.DAT_DATE >= '1990-01-01'
AND T_PAYS_PYS.PYS_NOM IN ('France', 'Germany', 'Ivory Coast', 'China', 'India', 'Denmark', 'United States')
AND T_DATA_DTA.DTA_NOM = 'GPD'
"""

pd.set_option('display.float_format', lambda x: '%.3f' % x)

df_datas_pib = pd.read_sql_query(requete_sql, conn)
df_datas_pib['DTA_VALEUR'] = pd.to_numeric(df_datas_pib['DTA_VALEUR'], errors='coerce')
df_datas_pib = df_datas_pib.dropna(subset=['DTA_VALEUR'])
df_datas_pib.columns = ['Year', 'Country', 'GDP']
df_datas_pib['Year'] = pd.to_datetime(df_datas_pib['Year']).dt.year.astype(str)

# Vérification des données
print("Exemple de données:")
print(df_datas_pib.head())

# Chargement des données GeoJSON
geojson_pays = 'https://raw.githubusercontent.com/datasets/geo-countries/master/data/countries.geojson'
geo_data = gpd.read_file(geojson_pays)

# Simplification des géométries pour réduire la taille
def simplifier_geometry(geometry, tolérance=0.01):
    return geometry.simplify(tolérance, preserve_topology=True)

geo_data['geometry'] = geo_data['geometry'].apply(simplifier_geometry)


# Assurer que les noms des pays correspondent exactement
mapping_pays = {
    'Ivory Coast': 'Côte d\'Ivoire',
    'United States': 'United States of America',
    'Germany': 'Germany',
    'France': 'France',
    'China': 'China',
    'India': 'India',
    'Denmark': 'Denmark'
}

df_datas_pib['Country'] = df_datas_pib['Country'].replace(mapping_pays)
# Création de la carte choroplèthe en utilisant Plotly
fig = go.Figure()

# Création des trames pour chaque année
années = df_datas_pib['Year'].unique()
trames = []
for année in années:
    données_trame = df_datas_pib[df_datas_pib['Year'] == année]
    trame = go.Choroplethmapbox(
        geojson=geo_data.__geo_interface__,
        locations=données_trame['Country'],
        z=données_trame['GDP'],
        featureidkey="properties.ADMIN",
        colorbar=dict(
            title='PIB',
        ),
        colorscale='Jet',
        hoverinfo='location+z',
        name=année
    )
    trames.append(go.Frame(data=[trame], name=année))

# Ajout des données initiales à la figure
données_initiales = df_datas_pib[df_datas_pib['Year'] == années[0]]
fig.add_trace(go.Choroplethmapbox(
    geojson=geo_data.__geo_interface__,
    locations=données_initiales['Country'],
    z=données_initiales['GDP'],
    featureidkey="properties.ADMIN",
    colorbar=dict(
        title='PIB',
    ),
    hoverinfo='location+z',
))

# Mise à jour de la mise en page pour inclure le curseur et les trames
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
                'label': 'Lecture',
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
            'prefix': 'Année:',
            'visible': True,
            'xanchor': 'right'
        },
        'transition': {'duration': 300, 'easing': 'cubic-in-out'},
        'pad': {'b': 10, 't': 50},
        'len': 0.9,
        'x': 0.1,
        'y': 0,
        'steps': [{
            'args': [[année], {'frame': {'duration': 300, 'redraw': True}, 'mode': 'immediate', 'transition': {'duration': 300}}],
            'label': year,
            'method': 'animate'
        } for year in années]
    }]
)

fig.frames = trames

# Save and display the map
fig.write_html('30YPIB.html')
fig.show()

