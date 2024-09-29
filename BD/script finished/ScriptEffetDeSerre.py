import pandas as pd
import pyodbc
import time

# Détails de connexion à la base de données
server = 'INFO-MSSQL-ETD'
database = 'SAE_TEAM5'
username = 'etd05'
password = 'fqnsbtc4'
fichiers = [
    'Z:\\Documents\\saeTruc\\csv\\edgar_processed_ch4_n2o_co2_fgasesTranslatedMieux.csv',
]

def process_chunk(df_chunk, conn, batch_size=100):
    cursor = conn.cursor()
    batch = []

    # Agréger les données par pays, année, secteur et gaz
    aggregated_df = df_chunk.groupby(
        ['country_code_a3', 'country_name', 'region_name', 'sector', 'gas', 'year', 'source']
    ).agg({'value_mteqco2': 'sum'}).reset_index()

    for index, row in aggregated_df.iterrows():
        value = round(float(row['value_mteqco2']), 6)
        country_code = row['country_code_a3']
        country_name = row['country_name']
        region_name = row['region_name']
        sector = row['sector']
        gas = row['gas']
        year = row['year']
        source = row['source']
        unit = gas

        # Ajouter les données au batch
        batch.append((country_code, country_name, region_name, sector, gas, year, value, source, unit))

        if len(batch) >= batch_size:
            # Insérer le batch
            insert_batch(batch, cursor)
            batch = []

    # Insérer le dernier batch restant
    if batch:
        insert_batch(batch, cursor)

    conn.commit()

def insert_batch(batch, cursor):
    for data in batch:
        country_code, country_name, region_name, sector, gas, year, value, source, unit = data

        try:
            if region_name:
                cursor.execute("""
                    IF NOT EXISTS (SELECT 1 FROM T_REGION_REG WHERE REG_NOM = ?)
                    BEGIN
                        INSERT INTO T_REGION_REG (REG_NOM) VALUES (?)
                    END
                """, region_name, region_name)
                cursor.execute("SELECT REG_ID FROM T_REGION_REG WHERE REG_NOM = ?", region_name)
                region_id = cursor.fetchone()[0]
            else:
                region_id = None

            if country_name:
                cursor.execute("""
                    IF NOT EXISTS (SELECT 1 FROM T_PAYS_PYS WHERE PYS_NOM = ?)
                    BEGIN
                        INSERT INTO T_PAYS_PYS (REG_ID, PYS_NOM) VALUES (?, ?)
                    END
                """, country_name, region_id, country_name)
                cursor.execute("SELECT PYS_ID FROM T_PAYS_PYS WHERE PYS_NOM = ?", country_name)
                country_id = cursor.fetchone()[0]
            else:
                country_id = None

            if sector:
                cursor.execute("""
                    IF NOT EXISTS (SELECT 1 FROM T_ACTIVITY_ACT WHERE ACT_NOM = ?)
                    BEGIN
                        INSERT INTO T_ACTIVITY_ACT (ACT_NOM) VALUES (?)
                    END
                """, sector, sector)
                cursor.execute("SELECT ACT_ID FROM T_ACTIVITY_ACT WHERE ACT_NOM = ?", sector)
                act_id = cursor.fetchone()[0]
            else:
                act_id = None

            cursor.execute("""
                IF NOT EXISTS (SELECT 1 FROM T_DATE_DAT WHERE DAT_DATE = ?)
                BEGIN
                    INSERT INTO T_DATE_DAT (DAT_DATE) VALUES (?)
                END
            """, f"{year}-01-01", f"{year}-01-01")
            cursor.execute("SELECT DAT_ID FROM T_DATE_DAT WHERE DAT_DATE = ?", f"{year}-01-01")
            date_id = cursor.fetchone()[0]

            # Vérifier si la combinaison existe déjà
            cursor.execute("""
                SELECT COUNT(*)
                FROM T_DATA_DTA
                WHERE PYS_ID = ? AND DAT_ID = ? AND ACT_ID = ? AND DTA_UNITE = ?
            """, country_id, date_id, act_id, unit)
            if cursor.fetchone()[0] == 0:
                cursor.execute("""
                    INSERT INTO T_DATA_DTA (PYS_ID, DAT_ID, DTA_VALEUR, DTA_NOM, DTA_UNITE, ACT_ID)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, country_id, date_id, value, "Emission Data", unit, act_id)
        except pyodbc.Error as e:
            print(f"Erreur lors de l'insertion des données : {e}")

def process_file(filename, conn, chunksize=1000):
    try:
        for chunk in pd.read_csv(filename, chunksize=chunksize):
            process_chunk(chunk, conn)
    except pd.errors.EmptyDataError:
        print("Le fichier est vide.")
    except pd.errors.ParserError as e:
        print(f"Erreur de lecture du fichier CSV : {e}")

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
    print(f"Erreur de connexion : {e}")
    exit()

# Mesure du temps de traitement
start_time = time.time()

# Traitement des fichiers
for fichier in fichiers:
    process_file(fichier, conn)

end_time = time.time()

print('finished')
print(f"Temps total utilisé : {end_time - start_time:.2f} secondes")
conn.close()
