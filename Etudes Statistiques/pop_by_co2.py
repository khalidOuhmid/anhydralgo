import matplotlib.pyplot as plt
import pandas as pd
import pymssql
import numpy as np
from scipy import stats

# Connexion à la base SAE_TEAM5
psw = 'fqnsbtc4'
usr = 'etd05'
dtbs = 'SAE_TEAM5'
cnxn = pymssql.connect(server='info-mssql-etd', user=usr,
                       password=psw, database=dtbs)
cursor = cnxn.cursor()

print('<- connected! ->')

theCommand = """
            SELECT pop.Year, pop.DTA_VALEUR AS Population, co2.Total_Valeur AS CO2_Consumption
            FROM (SELECT YEAR(DAT_DATE) AS Year, SUM(CAST(DTA_VALEUR AS float)) AS DTA_VALEUR 
                    FROM T_DATA_DTA
                    INNER JOIN 
                    T_PAYS_PYS ON T_DATA_DTA.PYS_ID = T_PAYS_PYS.PYS_ID
                    INNER JOIN 
                    T_DATE_DAT ON T_DATA_DTA.DAT_ID = T_DATE_DAT.DAT_ID
                    WHERE DTA_NOM = 'Population' AND PYS_NOM = 'France'
                    GROUP BY YEAR(DAT_DATE)
                    ) AS pop
            INNER JOIN (SELECT YEAR(DAT_DATE) AS Year, SUM(CAST(DTA_VALEUR AS float)) AS Total_Valeur
                        FROM T_DATA_DTA
                        INNER JOIN T_PAYS_PYS ON T_DATA_DTA.PYS_ID = T_PAYS_PYS.PYS_ID
                        INNER JOIN T_DATE_DAT ON T_DATA_DTA.DAT_ID = T_DATE_DAT.DAT_ID
                        WHERE DTA_UNITE = 'CO2' AND PYS_NOM = 'France'
                        GROUP BY YEAR(DAT_DATE)
                    ) AS co2
            ON pop.Year = co2.Year
            ORDER BY pop.Year;
            """

cursor.execute(theCommand)

# Récupération des résultats dans un DataFrame pandas
rows = cursor.fetchall()
df = pd.DataFrame(rows, columns=['Year', 'Population', 'CO2_Consumption'])

# Fermeture de la connexion
cnxn.close()

# Calcul de la régression linéaire
slope, intercept, r_value, p_value, std_err = stats.linregress(df['Population'], df['CO2_Consumption'])

# Affichage du graphique en nuage de points avec la régression linéaire
plt.figure(figsize=(15, 10))
plt.scatter(df['Population'], df['CO2_Consumption'], color='b', label='France', alpha=0.7)
plt.plot(df['Population'], intercept + slope * df['Population'], color='r', label='Régression linéaire')
plt.title('Population vs Consommation de CO2 en France avec régression linéaire')
plt.xlabel('Population')
plt.ylabel('Consommation de CO2')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig("pop_co2.png")
plt.show()

# Affichage des coefficients de la régression linéaire
print("========== Résultats de la Régression Linéaire ==========")
print(f"1. Coefficient de régression linéaire (pente) : {slope:.2f}")
print(f'2. Coefficient d\'interception : {intercept:.2f}')
print(f'3. Coefficient de corrélation (R²) : {r_value**2:.2f}')
print("=========================================================")