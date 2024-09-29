import matplotlib.pyplot as plt
import pandas as pd
import pymssql
import numpy as np
from matplotlib.ticker import ScalarFormatter   

# Connexion à la base SAE_TEAM5
psw = 'fqnsbtc4'
usr = 'etd05'
dtbs = 'SAE_TEAM5'
cnxn = pymssql.connect(server='info-mssql-etd', user=usr, password=psw, database=dtbs)
cursor = cnxn.cursor()

print('<- connected! ->')

def testGraph(cursor):
    command = """
    SELECT DTA_VALEUR, EGY_NOM, PYS_NOM, DAT_DATE
    FROM T_DATA_DTA
    INNER JOIN T_ENERGY_EGY ON T_ENERGY_EGY.EGY_ID = T_DATA_DTA.EGY_ID
    INNER JOIN T_DATE_DAT ON T_DATE_DAT.DAT_ID = T_DATA_DTA.DAT_ID
    INNER JOIN T_PAYS_PYS ON T_PAYS_PYS.PYS_ID = T_DATA_DTA.PYS_ID
    WHERE PYS_NOM = 'France'
        AND DAT_DATE BETWEEN '1990-01-01' AND '2024-12-31'
        AND EGY_NOM IN ('Coal', 'Gas', 'Hydro', 'Solar', 'Wind', 'Oil', 'Nuclear', 'Other renewables excluding bioenergy', 'Bioenergy')
    ORDER BY DAT_DATE
    """
    cursor.execute(command)
    rows = cursor.fetchall()
    
    # Convertir les données récupérées en DataFrame pandas
    df = pd.DataFrame(rows, columns=['DTA_VALEUR', 'EGY_NOM', 'PYS_NOM', 'DAT_DATE'])

    # Convertir DTA_VALEUR en numérique, forcer les erreurs à NaN puis les supprimer
    df['DTA_VALEUR'] = pd.to_numeric(df['DTA_VALEUR'], errors='coerce')
    df.dropna(subset=['DTA_VALEUR'], inplace=True)

    # Agréger les valeurs par nom d'activité
    aggregated_data = df.groupby('EGY_NOM')['DTA_VALEUR'].sum()

    # Créer un graphique en secteurs
    plt.figure(figsize=(10, 7))
    wedges, _, autotexts = plt.pie(aggregated_data, labels=None, autopct='%1.1f%%', startangle=140)

    # Ajouter une légende avec un meilleur positionnement
    plt.legend(wedges, aggregated_data.index, title="Activités", loc="center left", bbox_to_anchor=(1, 0.5), fontsize='small')
    plt.title('Répartition de DTA_VALEUR par Activité pour la France (1990-2024)')
    plt.axis('equal')  # Un rapport d'aspect égal assure que le graphique en secteurs est circulaire.

    # Ajuster la disposition pour faire de la place pour la légende
    plt.tight_layout()

    plt.show()

testGraph(cursor)
