import matplotlib.pyplot as plt
import pandas as pd
import pymssql

# Connexion à la base SAE_TEAM5
psw = 'fqnsbtc4'
usr = 'etd05'
dtbs = 'SAE_TEAM5'
cnxn = pymssql.connect(server='info-mssql-etd', user=usr, password=psw, database=dtbs)
cursor = cnxn.cursor()

print('<- connected! ->')

def testGraph(cursor):
    command = """
    SELECT DAT_DATE, DTA_VALEUR
    FROM T_DATA_DTA
    INNER JOIN T_DATE_DAT ON T_DATE_DAT.DAT_ID = T_DATA_DTA.DAT_ID
    INNER JOIN T_PAYS_PYS ON T_DATA_DTA.PYS_ID = T_PAYS_PYS.PYS_ID
    WHERE PYS_NOM LIKE '%France%' AND DAT_DATE >= '1990-01-01 00:00:00.000' AND DTA_NOM = 'GPD'
    """
    cursor.execute(command)
    results = cursor.fetchall()
    df = pd.DataFrame(results, columns=['DAT_DATE', 'DTA_VALEUR'])

    # Convertis la colonne DAT_DATE en type datetime        
    df['DAT_DATE'] = pd.to_datetime(df['DAT_DATE'])



    # Crée le graphique
    plt.figure(figsize=(10, 6))
    plt.plot(df['DAT_DATE'], df['DTA_VALEUR'], marker='o', linestyle='-')
    plt.title('Évolution du PIB de la France depuis 1990')
    plt.xlabel('Date')
    plt.ylabel('PIB')
    plt.grid(True)
    
    # Inverse l'axe y
    plt.gca().invert_yaxis()
    
    plt.show()

testGraph(cursor)
