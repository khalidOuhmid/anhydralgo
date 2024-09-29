import pandas as pd
import pyodbc
import pycountry_convert as pc
from datetime import datetime
import time
# Détails de connexion
server = 'INFO-MSSQL-ETD'
database = 'SAE_TEAM5'
username = 'etd05'
password = 'fqnsbtc4'
fichiers = [
    'Z:\\Documents\\saeTruc\\processed_gdp_worldbankTranslated.csv',
]

continents = {
    'NA': 'North America',
    'SA': 'South America', 
    'AS': 'Asia',
    'OC': 'Australia',
    'AF': 'Africa',
    'EU': 'Europe',
    'WW': 'World'
}
cont = ['North America','South America','Asia','Australia','Africa','Europe','World','Caribbean',
        'demographic','Euro','conflict','poor','income','IBRD','IDA','countries','OECD','small','Small',
        'Bahamas','Channel','Dem','Rep','Curacao','Hong']

def get_Region(country_name):
    try:
        country_code = pc.country_name_to_country_alpha2(country_name, cn_name_format="default")
        continent_name = pc.country_alpha2_to_continent_code(country_code)
        return continents[continent_name]
    except KeyError as e:
        print(f"KeyError encountered: {str(e)}")
        return country_name
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
        return country_name

def get_region_and_country(filename):
    region_name = filename
    country_name = filename
    if region_name == "Cote d'Ivoire":
        country_name = 'Ivory Coast'
    if region_name == 'Gambia, The':
        country_name = 'Gambia'

    for continent in cont:
        if continent in region_name:
            return region_name, country_name
    else:
        region_name = get_Region(country_name)
        return region_name, country_name

def is_valid_date(year):
    try:
        datetime.strptime(f"{year}-01-01", "%Y-%m-%d")
        return True
    except ValueError:
        return False

def process_row(year, region, value, filename, conn):
    if not is_valid_date(year):
        print('=================================')
        print(value)
        print(f"Invalid date for year: {year}")
        return

    region_name, country_name = get_region_and_country(region)
    unit = 'DOLLARS'

    with conn.cursor() as cursor:
        try:
            if region_name:
                cursor.execute("""
                    IF NOT EXISTS (SELECT 1 FROM T_REGION_REG WHERE REG_NOM = ?)
                    BEGIN
                        INSERT INTO T_REGION_REG (REG_NOM) VALUES (?)
                    END
                """, region_name, region_name)
                conn.commit()

                cursor.execute("SELECT REG_ID FROM T_REGION_REG WHERE REG_NOM = ?", region_name)
                row = cursor.fetchone()
                if row:
                    region_id = row[0]
                else:
                    region_id = None
            else:
                region_id = None

            if country_name:
                cursor.execute("""
                    IF NOT EXISTS (SELECT 1 FROM T_PAYS_PYS WHERE PYS_NOM = ?)
                    BEGIN
                        INSERT INTO T_PAYS_PYS (REG_ID, PYS_NOM) VALUES (?, ?)
                    END
                """, country_name, region_id, country_name)
                conn.commit()

                cursor.execute("SELECT PYS_ID FROM T_PAYS_PYS WHERE PYS_NOM = ?", country_name)
                row = cursor.fetchone()
                if row:
                    country_id = row[0]
                else:
                    country_id = None
            else:
                country_id = None

            if country_id:
                cursor.execute("""
                    IF NOT EXISTS (SELECT 1 FROM T_DATE_DAT WHERE DAT_DATE = ?)
                    BEGIN
                        INSERT INTO T_DATE_DAT (DAT_DATE) VALUES (?)
                    END
                """, f"{year}-01-01", f"{year}-01-01")
                conn.commit()

                cursor.execute("SELECT DAT_ID FROM T_DATE_DAT WHERE DAT_DATE = ?", f"{year}-01-01")
                row = cursor.fetchone()
                if row:
                    date_id = row[0]
                else:
                    date_id = None

                if date_id:
                    cursor.execute("""
                        INSERT INTO T_DATA_DTA (PYS_ID, DAT_ID, DTA_VALEUR, DTA_NOM, DTA_UNITE)
                        VALUES (?, ?, ?, ?, ?)
                    """, country_id, date_id, value, "GPD", unit)
                    conn.commit()
        except pyodbc.Error as e:
              print(f"Erreur lors de l'insertion des données : {e}")

def process_file(filename, conn):
    df = pd.read_csv(filename, delimiter=',', names=['Code', 'Year', 'country_name', 'Value'], skiprows=1)
    
    for index, row in df.iterrows():
        if ( row['Value'] != 0 and row['Year']> 1990  ):
            process_row(row['Year'], row['country_name'], row['Value'], filename, conn)

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
start_time = time.time()
# Traitement des fichiers
for fichier in fichiers:
    process_file(fichier, conn)

End_time = time.time()
print('finished')
print(f"Temps total utilisé : {End_time - start_time:.2f} secondes")
conn.close()
