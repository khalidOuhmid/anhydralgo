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
    SELECT DTA_VALEUR, ACT_NOM, PYS_NOM, DAT_DATE
    FROM T_DATA_DTA
    INNER JOIN T_ACTIVITY_ACT ON T_ACTIVITY_ACT.ACT_ID = T_DATA_DTA.ACT_ID
    INNER JOIN T_DATE_DAT ON T_DATE_DAT.DAT_ID = T_DATA_DTA.DAT_ID
    INNER JOIN T_PAYS_PYS ON T_PAYS_PYS.PYS_ID = T_DATA_DTA.PYS_ID
    WHERE PYS_NOM = 'France'AND DAT_DATE BETWEEN '1990-01-01' AND '2024-12-31'
    ORDER BY DAT_DATE
    """
    cursor.execute(command)
    rows = cursor.fetchall()
    
    # Création d'un DataFrame pandas à partir des résultats de la requête
    df = pd.DataFrame(rows, columns=['DTA_VALEUR', 'ACT_NOM', 'PYS_NOM', 'DAT_DATE'])

        # Transformer DAT_DATE en type datetime
    df['DAT_DATE'] = pd.to_datetime(df['DAT_DATE'])

    # Créer un graphique à aires
    plt.figure(figsize=(10, 6))
    for activity, group in df.groupby('ACT_NOM'):
        plt.plot(group['DAT_DATE'], group['DTA_VALEUR'], label=activity)

    plt.xlabel('Date')
    plt.ylabel('Valeur')
    plt.title('Evolution des activités en France')
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Afficher le graphique
    plt.show()

testGraph(cursor)
